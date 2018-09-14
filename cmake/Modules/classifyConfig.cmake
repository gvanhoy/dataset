INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_CLASSIFY classify)

FIND_PATH(
    CLASSIFY_INCLUDE_DIRS
    NAMES classify/api.h
    HINTS $ENV{CLASSIFY_DIR}/include
        ${PC_CLASSIFY_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    CLASSIFY_LIBRARIES
    NAMES gnuradio-classify
    HINTS $ENV{CLASSIFY_DIR}/lib
        ${PC_CLASSIFY_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(CLASSIFY DEFAULT_MSG CLASSIFY_LIBRARIES CLASSIFY_INCLUDE_DIRS)
MARK_AS_ADVANCED(CLASSIFY_LIBRARIES CLASSIFY_INCLUDE_DIRS)

