#include <pybind11/pybind11.h>
#include <nlohmann/json.h>

namespace py = pybind11;

/**
 * Caster for nlohmann::json
 * todo extract to lib
 */

namespace pybind11::detail {

    template <> struct type_caster<nlohmann::json> {
    public:
        /**
         * This macro establishes the name 'json' in
         * function signatures and declares a local variable
         * 'value' of type json
         */
        PYBIND11_TYPE_CASTER(nlohmann::json, _("json"));

        /**
         * Conversion part 1 (Python -> C++)
         */
        bool load(handle obj, bool) {
            value = to_json_impl(obj);
            return !value.empty();
        }

        /**
         * Conversion part 2 (C++ -> Python)
         */
        static handle cast(nlohmann::json src, return_value_policy /* policy */, handle /* parent */) {
            return from_json_impl(src);
        }

    private:
         nlohmann::json to_json_impl(py::handle obj)
         {

            py::module py_json = py::module::import("json");

            return nlohmann::json::parse(static_cast<std::string>(
                py::str(py_json.attr("dumps")(obj))
            ));

#if __USE_DIRECT_JSON_IMPL__
//
// TODO: this version is crashing! Must be solve and optimize
//
            if (obj.is_none())
            {
              return {};
            }

            if (py::isinstance<py::bool_>(obj))
            {
                return obj.cast<bool>();
            }

            if (py::isinstance<py::int_>(obj))
            {
                return obj.cast<long>();
            }

            if (py::isinstance<py::float_>(obj))
            {
                return obj.cast<double>();
            }

            if (py::isinstance<py::str>(obj))
            {
                return obj.cast<std::string>();
            }

            if (py::isinstance<py::tuple>(obj) || py::isinstance<py::list>(obj))
            {
                nlohmann::json out;
                for (py::handle value: obj)
                {
                    out.push_back(to_json_impl(value));
                }
                return out;
            }
            if (py::isinstance<py::dict>(obj))
            {
                nlohmann::json out;
                for (py::handle key: obj)
                {
                    out[key.cast<std::string>()] = to_json_impl(obj[key]);
                }
                return out;
            }
            throw std::runtime_error("to_json not implemented for this type of object: ...");
#endif
        }

        static handle from_json_impl(const nlohmann::json& element) {
            if (element.is_null()) {
                return py::none().release();

            } else if (element.is_boolean()) {
                return py::bool_(element).release();

            } else if (element.is_number_integer()) {
                return py::int_((int64_t)element).release();

            } else if (element.is_number_unsigned()) {
                return py::int_((uint64_t)element).release();

            } else if (element.is_number_float()) {
                return py::float_((double)element).release();

            } else if (element.is_string()) {
                return py::str((std::string)element).release();

            } else if (element.is_array()) {
                py::list result;
                for (auto const& subelement: element) {
                    result.append(from_json_impl(subelement));
                }
                return result.release();

            } else if (element.is_object()) {
                py::dict result;
                for (auto it = element.begin(); it != element.end(); ++it) {
                    result[from_json_impl(it.key())] = from_json_impl(it.value());
                }
                return result.release();
            }

            throw std::runtime_error("Unsupported json type");
        }
    };
}
