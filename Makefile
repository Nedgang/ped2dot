all:
	./exec_ped2dot.py exemple_family.tfam
	dot -Tpng family_Ex_Emple.dot -o family_Ex_Emple.png

black:
	black exec_ped2dot.py
	black ped2dot/*
