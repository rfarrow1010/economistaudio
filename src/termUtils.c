#define PY_SSIZE_T_CLEAN
#include <Python/Python.h>
#include <ncurses.h>

#if PY_MAJOR_VERSION >= 3
#define PY3K
#endif

// credit to https://stackoverflow.com/questions/32295927/failed-c-extension-compilation-for-python
// for the preprocessor insights

/*
    Author: Ryan Farrow
    Date: 14 Jul 2020

    This C file extends the Python script to allow the use of ncurses in 
    the terminal. Using C because I wanted to try it and it has the best 
    documentation! (http://www.tldp.org/HOWTO/NCURSES-Programming-HOWTO/intro.html)

    Note: include uses Python/Python.h as this works for MacOS. Might not work for Linux.
    This is because MacOS treats it as a framework. Compiled with the following command:

    gcc -shared -o termUtils.so termUtils.c -framework Python
*/

// Python extension docs: https://docs.python.org/3.8/extending/extending.html
// note to self: if using malloc, call PyErr_NoMemory on failure to allow Python
// to handle the exception

/*
    termUtils_interface

    Creates the ncurses interface in the terminal and handles input. This function 
    is called in a forked process in the main script.
    The main script is equipped to handle the input given to it accordingly, so 
    this function can just return the input as appropriate. Track runtime is also 
    handled in the script.

    Input:
    (audioname, catstring, lastCall)

    Returns the keystroke input by the user. Default value is 0 for unexpected 
    problems.
*/
static PyObject *termUtils_interface(PyObject *self, PyObject *args) {
    // reading in the arguments

    // C string of tuple of args passed into function call
    const char *audioname, *catstring, *lastCall;
    int uin = 0;

    if (!PyArg_ParseTuple(args, "sss", &audioname, &catstring, &lastCall)) {
        return NULL;
    }

    // initialization instructions for ncurses
    initscr();                  // start ncurses
    cbreak();                   // take input without carriage return, allow interpretation of Ctrl-C
    noecho();                   // do not echo input
    keypad(stdscr, TRUE);       // allows use of function keys and directional keys

    // if there is a message from last call, display it here
    printw(lastCall);

    // produce general output two lines below top
    printw("\n\n");
    printw("Now playing: %s\n", audioname);
    printw("Press q to quit, right key -> to rewind/go back one track,\n");
    printw("or left key <- to jump to the next track.\n");
    printw("Want to jump to a section? Press that section's corresponding key in the table below.\n\n");

    // print the formatted string displaying the catalogue
    printw(catstring);

    // currently on:
    // http://www.tldp.org/HOWTO/NCURSES-Programming-HOWTO/scanw.html
    // http://www.tldp.org/HOWTO/NCURSES-Programming-HOWTO/keys.html

    refresh();

    uin = getch();

    // if uin is left key or right key, it needs to get converted to 
    // p (previous) or n (next) respectively
    // otherwise it cannot be ASCII interpreted
    if (uin == KEY_LEFT) {
        uin = 'p';
    }
    else if (uin == KEY_RIGHT) {
        uin = 'n';
    }

    endwin();
    // must be converted in script to type "chr" then type str for comparison
    return PyLong_FromLong(uin);
}

// method table
static PyMethodDef TermUtilsMethods[] = {
    {"interface", termUtils_interface, METH_VARARGS, 
    "Launch the ncurses interface."},
    {NULL, NULL, 0, NULL}   // sentinel
};

#ifdef PY3K
// python3 module definition/init
static struct PyModuleDef termutilsmodule = {
    PyModuleDef_HEAD_INIT,
    "termUtils",
    NULL,           // this is for documentation; currently have none
    -1,
    TermUtilsMethods
};

PyMODINIT_FUNC PyInit_termUtils(void) {
    return PyModule_Create(&termutilsmodule);
}
#else 
// python2 module definition/init
PyMODINIT_FUNC inittermutils() {
    Py_InitModule3("termutils", TermUtilsMethods, "mod doc");
}
#endif