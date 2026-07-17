from pathlib import Path
from typing import Union

import yaml


def test_infra_files_exist(nginx_dir_info: tuple[Path, str],
                           expected_nginx_files: set[str]):
    path, dir_name = nginx_dir_info
    nginx_dir_content = {obj.name for obj in path.glob('*') if obj.is_file()}
    missing_files = expected_nginx_files - nginx_dir_content
    action = 'create the file' if len(missing_files) < 2 else 'create the files'
    assert not missing_files, (
        f'Make sure to {action} `{"`, `".join(missing_files)}` '
        f'in the `{dir_name}/` directory.'
    )


def test_deploy_info_file_content(
        deploy_file_info: tuple[Path, str],
        deploy_info_file_content: dict[str, str],
        expected_deploy_info_file_content: dict[str, str]
):
    _, relative_path = deploy_file_info
    missing_content = {
        key: value for key, value in expected_deploy_info_file_content.items()
        if key not in deploy_info_file_content
    }
    action = 'contains' if len(missing_content) < 2 else 'contain'
    key_word_form = 'key' if len(missing_content) < 2 else 'keys'
    assert not missing_content, (
        f'Make sure file `{relative_path}` {action} '
        f'{", ".join(missing_content.values())}. To output this '
        f'information, use the {key_word_form} '
        f'`{"`, `".join(missing_content.keys())}`.'
    )


def test_backend_dockerfile_exists(backend_dir_info: tuple[Path, str],
                                   dockerfile_name: str):
    path, relative_path = backend_dir_info
    assert (path / dockerfile_name).is_file(), (
        f'Make sure a `{dockerfile_name}` file exists in the '
        f'`{relative_path}/` directory.'
    )


def test_backend_dokerfile_content(backend_dir_info: tuple[Path, str],
                                   dockerfile_name: str):
    path, _ = backend_dir_info
    with open(path / dockerfile_name, encoding='utf-8', errors='ignore') as f:
        dockerfile_content = f.read()
    expected_keywords = (
        'from', 'run',
        'cmd' if 'cmd' in dockerfile_content.lower() else 'entrypoint'
    )
    for keyword in expected_keywords:
        assert keyword in dockerfile_content.lower(), (
            f'Make sure {dockerfile_name} is configured for the '
            '`kittygram_backend` image.'
        )


def safely_load_yaml_file(path_to_file: Path) -> dict[str, Union[dict, str]]:
    with open(path_to_file, 'r', encoding='utf-8', errors='ignore') as stream:
        try:
            file_content = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise AssertionError(
                f'Make sure file `{path_to_file}` uses valid YAML '
                'syntax. Reading the file raised the following '
                'exception:\n'
                f'{exc.__class__.__name__}: {exc}'
            )
    return file_content


def test_workflow_file(base_dir: Path, workflow_file_name: str):
    path_to_file = base_dir / workflow_file_name
    assert path_to_file.is_file(), (
        f'Make sure the project root directory contains a '
        f'`{workflow_file_name}` file describing the Kittygram workflow.'
    )
    workflow = safely_load_yaml_file(path_to_file)
    assert workflow, (
        f'Make sure file `{workflow_file_name}` in the project root '
        'directory contains the project workflow configuration.'
    )


def test_requirements_location(backend_dir_info: tuple[Path, str]):
    backend_path, relative_backend_path = backend_dir_info
    requirements_file_name = 'requirements.txt'
    path_to_file = backend_path / requirements_file_name
    assert path_to_file.is_file(), (
        f'Make sure directory {relative_backend_path} contains the '
        f'dependencies file `{requirements_file_name}`.'
    )


def has_forbiden_keyword(file_content: dict[str, Union[dict, str]],
                         forbidden_keyword: str) -> bool:
    is_forbidden_keyword_used = False
    for key, value in file_content.items():
        if isinstance(value, dict):
            if has_forbiden_keyword(value, forbidden_keyword):
                is_forbidden_keyword_used = True
        if key == forbidden_keyword:
            return True
    return is_forbidden_keyword_used


def test_docker_compose_prod_file_exists(base_dir: Path,
                                         docker_compose_prod_file_name: str):
    path_to_file = base_dir / docker_compose_prod_file_name
    assert path_to_file.is_file(), (
        f'Make sure the project root directory contains a '
        f'`{docker_compose_prod_file_name}` file.'
    )
    compose = safely_load_yaml_file(path_to_file)
    assert compose, (
        f'Make sure file `{docker_compose_prod_file_name}` in the '
        'project root directory contains the run configuration.'
    )
    assert not has_forbiden_keyword(compose, 'build'), (
        f'Make sure file `{docker_compose_prod_file_name}` does not '
        'contain a `build` instruction.'
    )
