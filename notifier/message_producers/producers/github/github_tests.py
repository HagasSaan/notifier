import os

import pytest
from aioresponses import aioresponses
from django.core.exceptions import ValidationError
from pytest_mock import MockFixture

from helpers.messages_components import ExternalMessage
from .github import GithubRepository


@pytest.fixture
def f_github_repository() -> GithubRepository:
    return GithubRepository(
        'owner/repository',
        'valid_token',
    )


@pytest.fixture
def m_pulls_fixture() -> bytes:
    with open(
        (
            os.path.dirname(os.path.abspath(__file__)) +
            '/github_pulls_fixture.json'
        ), 'rb',
    ) as fixture:
        yield fixture.read()


@pytest.fixture
def m_responses(
    f_github_repository: GithubRepository,
    m_pulls_fixture: bytes,
) -> MockFixture:
    with aioresponses() as mocked:
        mocked.get(
            f_github_repository.URL_PULLS.format(repository=f_github_repository.name),
            body=m_pulls_fixture,
        )
        yield mocked


@pytest.mark.asyncio
async def test_github_get_pull_requests(
    f_github_repository: GithubRepository,
    m_responses: MockFixture,
) -> None:
    pull_requests = await f_github_repository.get_pull_requests()

    assert len(pull_requests) == 1
    pull_request = pull_requests[0]

    assert pull_request.html_url == 'https://github.com/tekliner/dsas/pull/3045'
    assert pull_request.title == 'IMD-8404: Facebook limit error'
    assert pull_request.url == 'https://api.github.com/repos/tekliner/dsas/pulls/3045'
    assert pull_request.updated_at == '2020-08-28T11:36:52Z'
    assert (
        len(pull_request.assignees) == 2
        and {
            assignee.login
            for assignee in pull_request.assignees
        } == {'vlmihnevich', '123phg'}
    )
    assert len(pull_request.labels) == 1 and pull_request.labels[0].name == 'Facebook'


@pytest.mark.asyncio
async def test_github_produce_external_messages(
    f_github_repository: GithubRepository,
    m_responses: MockFixture,
) -> None:
    messages = await f_github_repository.produce_external_messages()
    assert set(messages) == {
        ExternalMessage(
            sender='comeuplater',
            receiver='vlmihnevich',
            content=(
                'IMD-8404: Facebook limit error '
                '(https://github.com/tekliner/dsas/pull/3045)\n'
                'Labels: Facebook'
            ),
        ),
        ExternalMessage(
            sender='comeuplater',
            receiver='123phg',
            content=(
                'IMD-8404: Facebook limit error '
                '(https://github.com/tekliner/dsas/pull/3045)\n'
                'Labels: Facebook'
            ),
        ),
    }


def test_validate_params() -> None:
    repository_name = 'owner/repository'

    with aioresponses() as mocked:
        mocked.get(
            GithubRepository.URL_REPOSITORY.format(repository=repository_name),
            body=b'{"some_content":"about_repo"}',
        )
        GithubRepository.validate_params(
            {
                'name': repository_name,
                'token': 'valid_token',
            },
        )


def test_validate_params_should_raise_error() -> None:
    repository_name = 'owner/repository'

    with aioresponses() as mocked:
        mocked.get(
            GithubRepository.URL_REPOSITORY.format(repository=repository_name),
            body=b'{"message":"Bad credentials"}',
            status=401,
        )
        with pytest.raises(
            ValidationError,
            match=GithubRepository.BAD_CREDENTIALS_MESSAGE,
        ):
            GithubRepository.validate_params(
                {
                    'name': repository_name,
                    'token': 'fake_token',
                },
            )
