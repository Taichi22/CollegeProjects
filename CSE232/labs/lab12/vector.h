#include<algorithm>
#include<utility>
#include<stdexcept>
using std::swap;
using std::range_error;

namespace student
{
	template<typename T>
	class vector
	{
		private:
			T* data_;
			size_t capacity_;
			size_t size_;
			
		public:
			vector(size_t capacity=10);
			vector(vector& v);
			~vector();
			size_t capacity();
			size_t size();
			void push_back(T val);
			vector& operator=(vector& v);
			T& operator[](size_t val);
			T& front();
			T& back();
			void clear();
			T& pop_back();
	};
	
	template <typename T>
	vector<T>::vector(size_t capacity)
	{
		capacity_ = capacity;
		size_ = 0;
		data_ = new T[capacity_]();
	}
	
	template <typename T>
	vector<T>::vector(vector& v)
	{
		capacity_ = v.capacity_;
		size_ = v.size_;
		data_ = new T[capacity_]();
		
		for(size_t d = 0; d < size_; ++d)
		{
			data_[d] = v.data_[d];
		}
	}
	
	template <typename T>
	vector<T>::~vector()
	{
		delete [] data_;
		data_ = NULL;
	}
	
	template <typename T>
	size_t vector<T>::capacity()
	{
		return capacity_;
	}
	
	template <typename T>
	size_t vector<T>::size()
	{
		return size_;
	}
	
	template <typename T>
	void vector<T>::push_back(T val)
	{
		if(size_ >= capacity_)
		{
			T* new_data = new T[capacity_ * 2];
			
			for(size_t d = 0; d < size_; ++d)
			{
				new_data[d] = data_[d];
			}
			
			swap(this->data_, new_data);
			
			new_data = NULL;
			
			capacity_ *= 2;
		}
		
		data_[size_++] = val;
	}
	
	template <typename T>
	T& vector<T>::operator[](size_t val)
	{
		if(val < size_)
		{
			T& result(*(data_ + val));
			return result;
		}
		else
		{
			throw range_error("Index is out of range");
		}
	}
	
	template <typename T>
	vector<T>& vector<T>::operator=(vector<T>& v)
	{
		capacity_ = v.capacity_;
		size_ = v.size_;
		data_ = new T[capacity_]();
		
		for(size_t d = 0; d < size_; ++d)
		{
			data_[d] = v.data_[d];
		}
		
		return *this;
	}
	
	template <typename T>
	T& vector<T>::front()
	{
		if(size_ > 0)
		{
			T& first(*data_);
			return first;
		}
		else {
			throw range_error("Vector is empty.");
		}
	}
	
	template <typename T>
	T& vector<T>::back()
	{
		if(size_ > 0)
		{
			T& last(*(data_ + size_ - 1));
			return last;
		}
		else {
			throw range_error("Vector is empty.");
		}
	}
	
	template <typename T>
	void vector<T>::clear()
	{
		delete [] data_;
		size_ = 0;
		capacity_ = 0;
	}
	
	template <typename T>
	T& vector<T>::pop_back()
	{
		if(size_ > 0)
		{
			T& last(*(data_ + size_ - 1));
			T* del = &data_[size_ - 1];
			delete del;
			del = nullptr;
			--size_;
			
			if(size_ <= capacity_ / 2)
			{
				T* new_data = new T[capacity_ / 2]();
				
				swap(this->data_, new_data);
				delete [] new_data;
				new_data = nullptr;
				
				capacity_ /= 2;
			}
			
			return last;
		}
		else {
			throw range_error("Vector is empty.");
		}
	}
}
