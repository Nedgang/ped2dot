all:
	./exec_ped2dot.py exemple_family.tfam

black:
	black exec_ped2dot.py
	black ped2dot/*
