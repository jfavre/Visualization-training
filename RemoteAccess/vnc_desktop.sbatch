#!/bin/bash -l
#SBATCH --job-name=vncdesktop
#SBATCH --nodes=1
#SBATCH --account=csstaff
#SBATCH -t 00:30:00
##SBATCH --partition=debug
#SBATCH --reservation=interact_
#SBATCH -C gpu&startx

if [ \! -e $HOME/.vnc/passwd ] ; then
	echo "For your protection, please run 'vncpasswd' before using vnc"
	exit 1
fi
HOSTNAME=$(hostname)
i=`scontrol show hostname $SLURM_JOB_NODELIST`
PORT=1$(echo $i|awk -Fnid0 '{print $2}')
XTHOST=$(cat /etc/xthostname)

echo "VNC Server accepting connections on $PORT"
echo "On client machine:"
# when outside CSCS, must go through ela
echo "Linux client:   ssh -f -L $PORT:${i}.${XTHOST}:5901 $USER@ela.cscs.ch sleep 3600"
echo "Windows client: \"C:\Program Files\PuTTY\plink.exe\" -l $USER -L $PORT:${i}.${XTHOST}:5901 ela.cscs.ch sleep 3600"
#otherwise go straight to nid
#echo "ssh -f -L $PORT:localhost:5901 $USER@${i}.${XTHOST} sleep 3600"
echo "vncviewer localhost:$PORT"
sync

sync

srun -n1 /apps/daint/system/bin/startvncdesktop 1920x1080

