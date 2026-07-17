from http import HTTPStatus
from pathlib import Path

import requests


def _get_dockerhub_username(
        deploy_file_info: tuple[Path, str],
        deploy_info_file_content: dict[str, str],
        dockerhub_username_key) -> str:
    _, relative_path = deploy_file_info
    assert dockerhub_username_key in deploy_info_file_content, (
        f'Make sure file `{relative_path}` contains the key '
        f'`{dockerhub_username_key}`.'
    )
    return deploy_info_file_content[dockerhub_username_key]


def test_dockerhub_images_exist(
        deploy_file_info: tuple[Path, str],
        deploy_info_file_content: dict[str, str],
        dockerhub_username_key: str
        ) -> None:
    common_part_of_link_to_docker_hub = (
        'https://hub.docker.com/v2/namespaces/{username}/repositories/{image}/'
    )
    expected_docker_images = (
        'kittygram_backend', 'kittygram_frontend', 'kittygram_gateway'
    )
    docker_hub_username = _get_dockerhub_username(
        deploy_file_info, deploy_info_file_content, dockerhub_username_key
    )
    expected_status_code = HTTPStatus.OK
    for image in expected_docker_images:
        link = common_part_of_link_to_docker_hub.format(
            username=docker_hub_username,
            image=image
        )
        response = requests.get(link, timeout=10)
        assert response.status_code == expected_status_code, (
            'Make sure image '
            f'`{image}` is available in your DockerHub account. '
            'The image must be public.'
        )
