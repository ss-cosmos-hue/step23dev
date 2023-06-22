#pragma once

#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>

class City
{
public:
    float x_, y_;
    City(float x, float y) : x_(x), y_(y){};
};

std::vector<City> read_input(const std::string &filename);