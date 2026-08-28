import json


class ConfigArgumentError(ValueError):
    pass


def parse_new_variables(arguments):
    variables = {}
    index = 0

    while index < len(arguments):
        if arguments[index] != "-new_var":
            index += 1
            continue

        if index + 1 >= len(arguments):
            raise ConfigArgumentError("-new_var requires <name>:<value>")

        value = arguments[index + 1]

        if ":" not in value:
            raise ConfigArgumentError("invalid -new_var value '%s', expected <name>:<value>" % value)

        name, replacement = value.split(":", 1)

        if not name:
            raise ConfigArgumentError("-new_var name must not be empty")

        variables[name] = replacement
        index += 2

    return variables


def render_config(content, variables):
    if not variables:
        return content

    start = content.find("{")
    end = content.rfind("}")

    if start == -1 or end <= start:
        raise ConfigArgumentError("build configuration does not contain a JSON object")

    inner = content[start + 1:end]

    try:
        return "{" + inner.format(**variables) + "}"
    except KeyError as exception:
        raise ConfigArgumentError("missing -new_var value for '%s'" % exception.args[0]) from exception


def load_build_config(path, arguments=()):
    with open(path, "r", encoding="utf-8") as stream:
        content = stream.read()

    content = render_config(content, parse_new_variables(list(arguments)))
    return json.loads(content)
