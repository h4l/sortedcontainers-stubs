group "default" {
    targets = ["test", "lint"]
}

target "test" {
    name = "test_python-${replace(py, ".", "-")}"
    matrix = {
        py = ["3.8", "3.9", "latest"],
    }
    args = {
        PYTHON_VER = py == "latest" ? "slim" : "${py}-slim"
    }
    target = "test"
    no-cache-filter = ["test"]
    output = ["type=cacheonly"]
}

target "lint" {
    name = "lint-${lint_type}"
    matrix = {
        lint_type = ["flake8", "black", "isort", "mypy", "pyright"],
    }
    args = {
        PYTHON_VER = "slim"
    }
    target = "lint-${lint_type}"
    no-cache-filter = ["lint-${lint_type}"]
    output = ["type=cacheonly"]
}
