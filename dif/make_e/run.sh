for((i=0; i<7; i+=7 ))
do
{
	cd $((i))
	mpirun -np 4 lmp_mpi -in in.simulation & 
	cd ../$((i+1))
	mpirun -np 4 lmp_mpi -in in.simulation & 
	cd ../$((i+2))
	mpirun -np 4 lmp_mpi -in in.simulation & 
	cd ../$((i+3))
        mpirun -np 4 lmp_mpi -in in.simulation &
        cd ../$((i+4))
        mpirun -np 4 lmp_mpi -in in.simulation &
        cd ../$((i+5))
        mpirun -np 4 lmp_mpi -in in.simulation &
	cd ..
}
wait
done


