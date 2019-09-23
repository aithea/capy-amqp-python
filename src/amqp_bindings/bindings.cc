#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <stdio.h>
#include <optional>
#include <map>
#include <string>
#include <stdio.h>

namespace py = pybind11;
using namespace pybind11::literals;

static std::map<std::string, std::string> py_connect(const std::string& phrase)
{
    if (phrase.empty())
    {
        throw std::runtime_error("Phrase is empty...");
    }

    return {{"test","test"}};
}

PYBIND11_MODULE(__capy_amqp, m) {

    m.doc() = "Capy amqp module...";

    m.def(
        "__open",
        &py_connect,
        "Open connection",
        "phrase"_a
    );
}
