#include<algorithm>
#include<utility>
#include<stdexcept>
#include<list>
#include<ostream>
#include<string>
#include<initializer_list>
#include<type_traits>
#include<sstream>
using std::overflow_error;
using std::underflow_error;
using std::list;
using std::swap;
using std::ostream; using std::ostringstream;
using std::endl;
using std::string;
using std::initializer_list;
//using statments

//forward declares because it's not a bad thing to be sure.
template<typename T>
class BiStack;
template <typename T>
ostream& operator<<(ostream &, const BiStack<T> &);

//Actual class
template<typename T>
class BiStack{
      private:
            T* stack; //singular pointer = more math
            size_t size1_; // need to know where buffer 1 is
            size_t size2_; // buffer 2
            size_t max_; // max size. kind of useless
            size_t capacity_; //current capacity.
            void grow_and_copy(); //grow and copy private funct.
      public:
            BiStack(size_t init = 4, size_t max = 16); //construct
            BiStack(initializer_list<T> init_list, size_t max = 16); //construct from list
            BiStack(BiStack& bs);
            ~BiStack();
            size_t capacity();
            size_t size();
            size_t max();
            void push1(T in);
            void push2(T in);
            void convert(char&);
            void convert(T&);
            T top1();            
            T top2();
            void pop1();
            void pop2();
            bool empty1();
            bool empty2();
            //operator overloads
            BiStack& operator=(BiStack& bs);
            //inline friend dec. 
            friend ostream& operator<<(ostream& os, const BiStack<T>& bs){
                  size_t z = 0;
                  os << "Top1 ";
                  if(bs.size1_ > z){
                        os <<"index:"<< bs.size1_-1;
                  }else{
                        os << "empty";
                  }
                  os << endl <<"Top2 ";
                  if(bs.size2_ > z){
                        os << "index:" << (bs.capacity_ - bs.size2_);
                  }else{
                        os<< "empty";
                  }
                  os << endl << "Size:"<< bs.size1_+bs.size2_ << endl;
                  os << "Capacity:" << bs.capacity_;
                  os << endl;
                  //string conversion was hell. stringstream is now my goto. permanently.
                  //seriously though the recommendation in several places was to use specialized
                  //type based functions
                  ostringstream temp;
                  for(size_t i = 0; i < bs.capacity_; ++i){
                        temp << *(bs.stack + i);
                        temp << ",";
                  }
//make sure that comma goes away
                  if(temp.str() != ""){
                        os << temp.str().substr(0,temp.str().size() - 1);
//and flush for good measure
                        temp.flush();
                  }
                  return os;
            }
};
//Init class
template <typename T>
BiStack<T>::BiStack(size_t init, size_t max){
      max_ = max;
      capacity_ = init;
      size1_ = 0;
      size2_ = 0;
      stack = new T[capacity_];
}
//Init from list class
template <typename T>
BiStack<T>::BiStack(initializer_list<T> init_list, size_t max){
      size1_ = init_list.size();
      size2_ = 0;
      capacity_ = init_list.size();
      max_ = max;
      stack = new T[capacity_];
//pointers are iterators. and arrays. and literally everything in c++
//LITERALLY EVERYTHING
      std::copy(init_list.begin(), init_list.end(), stack);
}
//Copy construct
template <typename T>
BiStack<T>::BiStack(BiStack& bs){
      capacity_ = bs.capacity_;
      max_ = bs.max_;
      size1_ = bs.size1_;
      size2_ = bs.size2_;
      stack = new T[capacity_];
//got tired of copy's shenanigans
      for(size_t i = 0; i < capacity_; ++i){
            stack[i] = bs.stack[i];
      }
}
//Deletion
template <typename T>
BiStack<T>::~BiStack(){
      if(!stack){
            delete [] stack;
            stack = nullptr;
      }
}
//Copy operator
template <typename T>
BiStack<T>& BiStack<T>::operator=(BiStack& bs){
      capacity_ = bs.capacity_;
      max_ = bs.max_;
      size1_ = bs.size1_;
      size2_ = bs.size2_;
      stack = new T[capacity_];
//for loops are better than copy. sometimes.
//they are for sure clearer.
      for(size_t i = 0; i < capacity_; ++i){
            stack[i] = bs.stack[i];
      }
      return bs;
}
//Returns cap
template <typename T>
size_t BiStack<T>::capacity(){
      return capacity_;
}
//Returns size
template <typename T>
size_t BiStack<T>::size(){
      return size1_ + size2_;
}
//Returns max
template <typename T>
size_t BiStack<T>::max(){
      return max_;
}
//Pushes stuff into 1
template <typename T>
void BiStack<T>::push1(T in){
      if(stack){
            if(size1_ + size2_+1 <= capacity_){
//Increments while getting the right place.
                  stack [size1_++]= in;
            }else{
                  grow_and_copy();
//Ditto
                  stack[size1_ ++] = in;
            }
      }else{
            stack = new T[capacity_];
            stack [size1_++] = in;
      }
}
//Push into 2. Does math to make sure stuff goes where it's supposed to
template <typename T>
void BiStack<T>::push2(T in){
      if(stack){
            if(size1_ + size2_+1 <= capacity_){
                  stack [capacity_ - ++size2_]= in;
            }else{
                  grow_and_copy();
                  stack[capacity_ - ++size2_] = in;   
            }
      }else{
            size2_ = 0;
            stack = new T[capacity_];
            stack [capacity_ - ++size2_] = in;
      }
}
//Shows me what the top of the 1st stack is
template<typename T>
T BiStack<T>::top1(){
      T ret;
      if(stack && ((size1_ - 1) >= 0)){
            ret = stack[size1_-1];
      }else{
            throw underflow_error("underflow stack 1");
      }
      return ret;
}
//Ditto for second stack
template<typename T>
T BiStack<T>::top2(){
      T ret;
      if(stack[capacity_-size2_] != 0){
            ret = stack[capacity_ - size2_];
      }else{
            throw underflow_error("underflow stack 2");
      }
      return ret;
}
//pops off the 1st stack's most recent entry
template <typename T>
void BiStack<T>::pop1(){
      if(stack){
            stack[size1_] = 0;
            --size1_;
      }else{
            throw underflow_error("underflow stack 1");
      }
}
//Ditto, again.
template <typename T>
void BiStack<T>::pop2(){
      if(stack[capacity_-size2_]){
            stack[capacity_ - size2_] = 0;
            -- size2_;
      }else{
            throw underflow_error("underflow stack 2");
      }
}
//Checks for empty stack. kind of inefficient but stacks are private, so...
template <typename T>
bool BiStack<T>::empty1(){
      return (!stack);
}
//Ditto for 2.
template <typename T>
bool BiStack<T>::empty2(){
      return (!stack[capacity_ - size2_]);
}
//The big boy.
//I ended up reworking arithmetic for this several times.
//It copies all of stack 1 in, then copies stack 2 an appropriate distance away.
template<typename T>
void BiStack<T>::grow_and_copy(){
      if(capacity_ < max_){
            T* temp = new T[capacity_ * 2];
            size_t newcap = capacity_ * 2;
            std::copy(stack, (stack+size1_+1), temp);
            std::copy((stack + capacity_ -size2_), (stack + (capacity_)), 
                  (temp + newcap - size2_));
            capacity_ = newcap;
            swap(temp, stack);
            delete [] temp;
            temp = nullptr;
      }else{
            throw overflow_error("stack past max");
      }
}
