import asyncio
import dataclasses
import json
from typing import List, Union, Dict, Any

import aiohttp
import structlog
from django.core.exceptions import ValidationError
from django.db.models import JSONField

from helpers.traits import Initable
from helpers.registry import Registry
from ..message_producer import PRODUCER_REGISTRY_NAME, ExternalMessage, MessageProducer

logger = structlog.get_logger(__name__)


class GithubUser(Initable):
    login: str


class GithubLabel(Initable):
    name: str

    def __str__(self):
        return self.name


class GithubPullRequest(Initable):
    url: str
    html_url: str
    title: str
    user: GithubUser
    updated_at: str
    labels: List[GithubLabel]
    assignees: List[GithubUser]

    # approved_by: Set[str] = field(default_factory=set)  # noqa: E800
    # reviewers: Dict[str, str] = field(default_factory=dict)  # noqa: E800


@Registry.register(PRODUCER_REGISTRY_NAME)
@dataclasses.dataclass
class GithubRepository(MessageProducer):
    # TODO: make token optional param
    name: str
    token: str

    USERNAME_KEY = 'github_username'

    URL_API_GITHUB = 'https://api.github.com'
    URL_REPOSITORY = URL_API_GITHUB + '/repos/{repository}'
    URL_PULLS = URL_REPOSITORY + '/pulls'

    BAD_CREDENTIALS_MESSAGE = 'Bad credentials'

    @classmethod
    def validate_params(cls, params: Union[Dict, JSONField]) -> None:
        try:
            asyncio.run(
                cls(**params)._request(
                    cls.URL_REPOSITORY.format(repository=params['name']),
                ),
            )
        except Exception as e:
            if cls.BAD_CREDENTIALS_MESSAGE in str(e):
                raise ValidationError(cls.BAD_CREDENTIALS_MESSAGE)
            raise e

    async def produce_messages(self) -> List[ExternalMessage]:
        messages: List[ExternalMessage] = []
        pull_requests = await self.get_pull_requests()
        for pull_request in pull_requests:
            for pull_request_assignee in pull_request.assignees:
                message = ExternalMessage(
                    sender=pull_request.user.login,
                    receiver=pull_request_assignee.login,
                    content=(
                        f'{pull_request.title} '
                        f'({pull_request.html_url})'
                        f'\nLabels: {",".join(map(str,pull_request.labels))}'
                    ),
                )
                messages.append(message)

        return messages

    async def get_pull_requests(self) -> List[GithubPullRequest]:
        pull_requests = list(map(
            GithubPullRequest,
            await self._request(
                self.URL_PULLS.format(repository=self.name),
            ),
        ))
        logger.info('Pull requests downloaded')
        return pull_requests

    async def _request(self, url: str) -> Dict[str, Any]:
        async with aiohttp.request(
            'get', url,
            headers={'Authorization': f'Bearer {self.token}'},
        ) as response:
            logger.info('Got response', status_code=response.status, url=url)
            content = await response.content.read()
            decoded_content = json.loads(content.decode())
            if response.status != 200 or not content:
                raise Exception(
                    f'Bad response, '
                    f'status code: {response.status}, '
                    f'content: {decoded_content}',
                )

            return decoded_content
