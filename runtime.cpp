#include <iostream>
#include <cstring>
#include <cstdlib>

extern "C" {
    // Print double number
    void dhicode_print_num(double val) {
        std::cout << val << std::endl;
    }

    // Print UTF-8 string
    void dhicode_print_str(const char* val) {
        if (val) {
            std::cout << val << std::endl;
        }
    }

    // Print boolean (in Dhivehi: އާން / ނޫން)
    void dhicode_print_bool(int val) {
        if (val) {
            std::cout << "އާން" << std::endl;
        } else {
            std::cout << "ނޫން" << std::endl;
        }
    }

    // String concatenation
    char* dhicode_concat_str(const char* s1, const char* s2) {
        if (!s1) s1 = "";
        if (!s2) s2 = "";
        size_t len1 = strlen(s1);
        size_t len2 = strlen(s2);
        char* res = (char*)malloc(len1 + len2 + 1);
        if (res) {
            memcpy(res, s1, len1);
            memcpy(res + len1, s2, len2);
            res[len1 + len2] = '\0';
        }
        return res;
    }

    // Input prompt
    char* dhicode_input_str(const char* prompt) {
        if (prompt && strlen(prompt) > 0) {
            std::cout << prompt;
        }
        std::string input;
        if (std::getline(std::cin, input)) {
            char* res = (char*)malloc(input.size() + 1);
            if (res) {
                memcpy(res, input.c_str(), input.size());
                res[input.size()] = '\0';
            }
            return res;
        }
        return nullptr;
    }
}
