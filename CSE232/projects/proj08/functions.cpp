/*

 * File: Functions.cpp

 * Author: Brian Cong

 * Assignment: CSE 232 Project08

 * 

 * Created March 23,2017

 */
#include <vector>

using std::vector;

#include <iostream>

using std::cout;using std::cin;using std::endl;
#include<sstream>
using std::ostringstream;
#include<string>
using std::string;
#include<map>
using std::map;
#include<cmath>
#include<array>
#include<stdexcept>

#include "functions.h"

string Node::to_string () const{
	ostringstream oss;
	oss<< label << ":(" <<  x << "," << y << ")";
	return oss.str();
}
bool Node::equal_nodes(const Node &n){
	if(label == n.label){ return true;} else {return false;}
}
double Node::distance(const Node &n)const{
	double ret;
	ret = std::sqrt(pow(double(x + n.x),2)+pow(double(y+n.y),2));
	return ret;
}
Network::Network(ifstream &ifs){
	Network net;
	//If I'm understanding the code correctly, getline
	//will store the characters in the line(deliminated by '\n') to the array a
	//getline(char_type*s, std::streamsize count, char_type delim) imply that
	//getline will store characters of streamsize count amount, deliminated by char_type characters, into s
	//This is, of course, assuming that getline is inherited by ifstream from istream.
	//According to cppreference, the following loop will terminate when the ifs.getline returns a false std::ios_base::operator bool().
	for(std::array<char, 6> a; ifs.getline(&a[0], 4, '\n');){
		string label = a[5]+a[6];
		Node n(int(a[0]), int(a[3]), label);
		net.put_node(n);
	}
}
string Network::to_string () const{
	ostringstream oss;
	for(auto a:nodes){
		oss << a.second.to_string() << ",";
	}
	return oss.str();
}
Node Network::get_node(string l){
	for(auto a: nodes){
		if(a.second.label == l){
			return a.second;
		}else{
			throw std::out_of_range ("Out of range.");
		}
	}
}
void Network::put_node(Node n){
	nodes[n.label] = n;
}
bool Network::in_route(const Node&n){
	if(route.find(label) != route.end()){
	//route contains label
		return true;
	}else{
	//route does not contain label
		return false;
	}
}
Node Network::closest(Node &n){
	Node ret;
	double mindist = 9999999;
	for(auto a:nodes){
		double cur = sqrt(pow(double(a.second.x + n.x),2) + pow(double(a.second.y + n.y),2));
		if(cur < mindist){
			mindist = cur;
			ret = a.second;
		}
	}
	return ret;
}
string Network::calculate_route(const Node&start, const Node&end){
	route.push_back(start);
	Node cur = start;
	double totaldist = 0;
	while(!end.equal_nodes(cur)){
		totaldist += cur.distance(closest(cur));
		cur = closest(cur);
		route.push_back(cur);
		
	}
}
