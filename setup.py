import os
import platform
import subprocess
import sys

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

__version__ = '0.3.1'
__capy_amqp_version__ = '0.5.4'

darwin_flags = ['-mmacosx-version-min=10.14', '-faligned-allocation']
cmake_darwin_flags = ['-DOPENSSL_ROOT_DIR=/usr/local/opt/openssl']


def pull_external(name, url, branch=None):
    if not os.path.isdir("src/external/"+name):
        subprocess.check_call(
            ['git', "clone", url, "src/external/"+name],
            env=os.environ.copy())
    else:
        subprocess.check_call(
            ['git', "-C", "src/external/"+name, "pull"],
            env=os.environ.copy())

    if branch:
        subprocess.check_call(
            ['git', "-C", "src/external/" + name, "checkout", branch],
            env=os.environ.copy())


class ExtensionWithLibrariesFromSources(Extension):
    """Win is unsupported"""

    def __init__(self, name, sources, *args, **kw):
        self.libraries_from_sources = kw.pop('libraries_from_sources', [])

        if platform.system() == 'Darwin':
            kw['extra_link_args'] = kw.get('extra_link_args', []) + darwin_flags
            kw['include_dirs'] = kw.get('include_dirs', []) + [
                '/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include/c++/v1'
            ]

        pull_external("amqpcpp", "https://github.com/dnevera/AMQP-CPP")

        pull_external("capy-dispatchq", "https://github.com/aithea/capy-dispatchq")

        pull_external("capy-common-cpp", "https://github.com/aithea/capy-common-cpp")

        pull_external("capy-amqp-cpp", "https://github.com/aithea/capy-amqp-cpp", 'feature/capy-common-cpp')

        pull_external("pybind11", "https://github.com/pybind/pybind11")

        super().__init__(name, sources, *args, **kw)

    def build_libraries(self, ext_builder: build_ext):
        self.check_cmake_version()

        libraries = []
        libraries_dirs = ['/usr/lib']

        for lib_name, lib_path, lib_version in self.libraries_from_sources:
            libraries += [lib_name]
            libraries_dirs += self.build_library(
                ext_builder, lib_name, os.path.abspath(lib_path), lib_version
            )

        print(libraries, libraries_dirs)

        return libraries, libraries_dirs

    @staticmethod
    def build_library(ext_builder: build_ext, lib_name, lib_path, lib_version):
        build_temp = os.path.join(ext_builder.build_temp, lib_name)

        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + build_temp,
                      '-DPYTHON_EXECUTABLE=' + sys.executable]

        cfg = 'Debug' if ext_builder.debug else 'Release'
        build_args = ['--config', cfg]

        cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]

        if platform.system() == 'Darwin':
            cmake_args += cmake_darwin_flags

        build_args += ['--', '-j1']

        env = os.environ.copy()

        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(
            env.get('CXXFLAGS', ''), lib_version
        )

        if not os.path.exists(build_temp):
            os.makedirs(build_temp)

        subprocess.check_call(['cmake', lib_path] + cmake_args,
                              cwd=build_temp, env=env)

        subprocess.check_call(['cmake', '--build', '.'] + build_args,
                              cwd=build_temp)

        return [build_temp, build_temp + '/lib', build_temp + '/bin']

    def check_cmake_version(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extension: " + self.name
            )


class BuildExt(build_ext):
    def build_extension(self, ext: Extension):
        if type(ext) is ExtensionWithLibrariesFromSources:
            ext: ExtensionWithLibrariesFromSources
            libraries, library_dirs = ext.build_libraries(self)
            ext.libraries += libraries
            ext.library_dirs += library_dirs
        super().build_extension(ext)


extra_compile_args = ['-std=c++17', '-DVERSION_INFO="{}"'.format(__version__)]

if platform.system() == 'Darwin':
    extra_compile_args = extra_compile_args + darwin_flags

ext_modules = [
    ExtensionWithLibrariesFromSources(
        '__capy_amqp',
        ['./src/amqp_bindings/bindings.cc'],
        include_dirs=[
            'src/external/amqpcpp/include',
            'src/external/capy-dispatchq/include',
            'src/external/capy-common-cpp/include',
            'src/external/capy-common-cpp/external',
            'src/external/capy-amqp-cpp/include',
            'src/external/capy-amqp-cpp/external',
            'src/external/pybind11/include',
            '/usr/include',
            '/usr/local/include',
        ],
        language='c++',
        extra_compile_args=extra_compile_args,
        libraries_from_sources=[
            ("capy_common_cpp", 'src/external/capy-common-cpp', __capy_amqp_version__),
            ("capy_dispatchq", 'src/external/capy-dispatchq', __capy_amqp_version__),
            ("amqpcpp", 'src/external/amqpcpp', __capy_amqp_version__),
            ("capy_amqp_cpp", 'src/external/capy-amqp-cpp', __capy_amqp_version__),
        ],
        libraries=['amqpcpp', 'capy_amqp_cpp', 'ssl', 'uv', 'z', 'amqpcpp', 'uv'],
    ),
]

setup(

    cmdclass={
        'build_ext': BuildExt,
    },

    name='capy_amqp',

    version=__version__,

    author="AIthea",

    license="MIT",

    description='Python Package AMQP C Extension',

    url="http://aithea.com/",

    packages=['capy_amqp'],

    ext_modules=ext_modules,

    install_requires=[
        'urllib3',
        'requests'
    ],

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ]
)
