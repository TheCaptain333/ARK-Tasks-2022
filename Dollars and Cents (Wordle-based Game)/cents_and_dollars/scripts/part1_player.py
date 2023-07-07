#!/usr/bin/env python3
from part1_checker import noDuplicates
import rospy
import std_msgs
from std_msgs.msg import Int64
import numpy as np
import os
import sys


pub = rospy.Publisher('/guess_part1', Int64, queue_size=100)
n = rospy.get_param("/centsdollars1/digits")
digit_list = list('0123456789')
global num
num = 0

global dollars
global cents
global new_dollars
global new_cents
global new_dollarcent
global old1
global old2


for x in range(1,n+1):
	num*=10
	num+=(x%10)
	

def dollarcentCallback(data):
    global new_dollarcent
    new_dollarcent = data.data

def try_number(numstr):
	
	
	global new_dollars
	global new_cents
	global new_dollarcent
	pub.publish(numstr)
	rospy.sleep(0.1)
	
	if(new_dollarcent==999):sys.exit()
	
	if(n < 10):
		new_dollars = new_dollarcent//10	
		new_cents = new_dollarcent%10
		
	else:
		new_dollars = (new_dollarcent-10)//9
		new_cents = (100-new_dollarcent)//9
	return new_dollars,new_cents
	
def try_swap(numstr,i,j):

	numstr[i],numstr[j] = numstr[j],numstr[i]
	
	new_num = int("".join(numstr))
	
	try_number(new_num)
	return new_num

def diff():
	global dollars
	global cents
	global new_dollars
	global new_cents
	global old1
	global old2

	old1 = dollars
	old2 = cents
	
	dollars = new_dollars
	cents = new_cents	
	return new_dollars-old1,new_cents-old2

def revert_back():
	global dollars
	global cents
	global old1
	global old2
	
	dollars = old1
	cents = old2


def remove_unwanted_digits():
	global dollars
	global cents
	global num
	
	for i in range(0,n):
		num_list = list(str(num))
		if(dollars+cents==n):
			break
		for item in list(set(digit_list)-set(num_list)):
			if(i==0 and item=='0'):
				continue
			num_list[i]=item
			string_new = "".join(num_list)
			try_number(int(string_new))
			del_d,del_c = diff()
			if(del_d+del_c > 0):
				num = int(str(string_new))
				break
			else:
				revert_back()
	
	
	
	
def reorder_digits():
	print('All unwanted digits removed')
	global num

	for i in range(0,n):
		dict_nd={}
		for j in range(i+1,n):
			if(i==0 and list(str(num))[j]=='0'):continue
			try_swap(list(str(num)),i,j)
			del_d,del_c = diff()
			dict_nd[j]=del_d
			revert_back()
		if(2 in dict_nd.values()):
			for key,value in dict_nd.items():
				if(value==2):
					num = try_swap(list(str(num)),i,key)
					diff()
					break
			continue
		
		neg_list = [i for i in dict_nd.values() if i < 0]
		
		if(len(neg_list)==len(dict_nd.values())):continue
		
		special_indices=list()
		
		for key,value in dict_nd.items():
			if(value==1): special_indices.append(key)
			
		
			
		
		num = try_swap(list(str(num)),i,special_indices[0])
		diff()
		
		if(len(special_indices)==1):
			continue
		
		num_temp=try_swap(list(str(num)),i,special_indices[1])
		del_d2,del_c2 = diff()
		
		if(del_d2>0): 
			
			num = num_temp
		
		else: 
			
			revert_back()
		
			
		
	
def play():
    
    global dollars
    global cents
    global new_dollars
    global new_cents
    
    
    rospy.init_node('player1')
    
    rospy.Subscriber("/check1", Int64, dollarcentCallback)
    rospy.sleep(1)
    try_number(num)
    
    dollars = new_dollars
    cents = new_cents
    
    remove_unwanted_digits()
    reorder_digits()
    
    	

if __name__ == '__main__':
    try:
        play()
    except rospy.ROSInterruptException:
        pass
