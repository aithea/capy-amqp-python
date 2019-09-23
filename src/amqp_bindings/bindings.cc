#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <nlohmann/json.h>

#include <stdio.h>
#include <optional>
#include <functional>
#include <map>
#include <string>
#include <stdio.h>

#include "cast_json.h"
#include "capy/amqp.h"

namespace py = pybind11;
using namespace pybind11::literals;

struct FetchHandler {

    virtual void on_data(const nlohmann::json& data) const {}
    virtual ~FetchHandler() {}

};

struct PyFetchHandler : public FetchHandler {

public:
    /* Inherit the constructors */
    using FetchHandler::FetchHandler;

    /* Trampoline (need one for each virtual function) */
    void on_data(const nlohmann::json& data) const override {
        PYBIND11_OVERLOAD_PURE(
            void,            /* Return type */
            FetchHandler,    /* Parent class */
            on_data,         /* Name of function in C++ (must match Python name) */
            data             /* Argument(s) */
        );
    }
};

class PyBroker {


public:

    PyBroker(const std::string& url):url_(url){}
    const std::string& get_url() const {  return url_; }
    void set_url(const std::string& url) { url_ = url; }

    void fetch (const nlohmann::json& message,
                const std::string& routing_key,
                const FetchHandler* handler) {
         handler->on_data(message);
    }

private:
     std::string url_;
};

static std::unique_ptr<PyBroker> py_bind(const std::string& url)
{
    if (url.empty())
    {
        throw std::runtime_error("Address is empty...");
    }

    return std::unique_ptr<PyBroker>(new PyBroker(url));
}

PYBIND11_MODULE(__capy_amqp, m) {

    m.doc() = "Capy amqp module...";

    m.def(
        "Bind",
        &py_bind,
        "Bind amqp queue",
        "url"_a
    );

    py::class_<FetchHandler, PyFetchHandler >(m, "FetchHandler")
        .def(py::init<>())
        .def("on_data", &FetchHandler::on_data);

    py::class_<PyBroker> py_broker_class(m, "Broker");
    py_broker_class
        .def(py::init<std::string>())
        .def("fetch", &PyBroker::fetch)
        .def_property("url", &PyBroker::get_url, &PyBroker::set_url);
}
