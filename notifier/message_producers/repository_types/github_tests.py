import pytest
from aioresponses import aioresponses
from django.core.exceptions import ValidationError

from message_producers.repository_types.github import GithubRepository


@pytest.fixture
def f_github_repository() -> GithubRepository:
    return GithubRepository(
        'owner/repo',
        'api_token',
    )


@pytest.mark.skip(reason='Need to mock request first')
@pytest.mark.asyncio
async def test_github_get_pull_requests(f_github_repository: GithubRepository) -> None:
    pull_requests = await f_github_repository.get_pull_requests()
    assert pull_requests


@pytest.mark.skip(reason='Need to mock request first')
@pytest.mark.asyncio
async def test_github_produce_messages(f_github_repository: GithubRepository) -> None:
    messages = await f_github_repository.produce_messages()
    assert messages


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
