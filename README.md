# Symbolic-Parser
I have designed a symbolic parsing algorithm. It has numerous applications. This repository contains one such application, repair of 
buggy token sequence. Given any program, it will repair the compilation errors automatically. The parsing algorithm is a general algorithm
 which can be used for any LL(k) grammar, but for simplicity I have implemented for LL(1) grammar. The tool is independent of the 
 language used, as it requires grammar of the language as input.
 The repository contains the followin modules:
 * Lexer
 * Error Generator: It introduces replacement, deletion and insertion errors in the program. Number of errors generated can be controlled 
 by specifying the probability of generating an error. Also, user can control the probability of generating insertion, deletion and replacement errors.
 * Top-down parser
 * Symbolic Parser
 * end-to-end Repair tool
 The whole tool is implemented in Python using the *Microsoft's Z3Py* API.
