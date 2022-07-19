cmake_minimum_required(VERSION 3.0.0)
project(FIND_FILE VERSION 0.1.0)

include(CTest)
enable_testing()

add_executable(main main.cpp cc_util.cpp cc_util.hpp)
set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
find_package(OpenCV REQUIRED QUIET)

target_link_libraries(main ${OpenCV_LIBS})

