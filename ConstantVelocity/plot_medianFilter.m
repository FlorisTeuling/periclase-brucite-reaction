clear all; close all; clc

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

chdir('03_22_NoWater')

[NoWater data_forces_NW] = read_1040('forces.txt', 2, ' ');
[NoWater data_distance_NW] = read_1040('cube.z.txt', 2, ' ');

fx_NW = data_forces_NW(:,2); Px_NW = (fx_NW * 1.43935*10^-4)*((4.217*9)*(4.217*9));
fy_NW = data_forces_NW(:,3); Py_NW = (fy_NW * 1.43935*10^-4)*((4.217*9)*(4.217*9));
fz_NW = data_forces_NW(:,4); Pz_NW = (fz_NW * 1.43935*10^-4)*((4.217*9)*(4.217*9));

timestep_NW = data_distance_NW(:,1) * 2 * 10^-6 ; %ns
deltaZ_NW = data_distance_NW(:,4); deltaZ_NW = deltaZ_NW-2.5;

a=0;
for i = 1:1000:length(deltaZ_NW)
    a=a+1;
    deltaz2_NW(a) = mean(deltaZ_NW(i):deltaZ_NW(i)+999);
end

chdir('..')


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

chdir('03_23_WithWater_Fram')

[Water1 data_forces_Water1] = read_1040('forces.txt', 2, ' ');
[Water1 data_distance_Water1] = read_1040('cube.z.txt', 2, ' ');

fx_Water1 = data_forces_Water1(:,2); Px_Water1 = (fx_Water1 * 1.43935*10^-4)*((4.217*9)*(4.217*9));
fy_Water1 = data_forces_Water1(:,3); Py_Water1 = (fy_Water1 * 1.43935*10^-4)*((4.217*9)*(4.217*9));
fz_Water1 = data_forces_Water1(:,4); Pz_Water1 = (fz_Water1 * 1.43935*10^-4)*((4.217*9)*(4.217*9));

timestep_Water1 = data_distance_Water1(:,1) * 2 * 10^-6 ; %ns
deltaZ_Water1 = data_distance_Water1(:,4); deltaZ_Water1 = deltaZ_Water1-2.5;

a=0;
for i = 1:1000:length(deltaZ_Water1)
    a=a+1;
    deltaz2_Water1(a) = mean(deltaZ_Water1(i):deltaZ_Water1(i)+999);
end

chdir('..')


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


chdir('03_26_WithWater')

[Water2 data_forces_Water2]   = read_1040('forces.txt', 2, ' ');
[Water2 data_distance_Water2] = read_1040('cube.z.txt', 2, ' ');

fx_Water2 = data_forces_Water2(:,2); Px_Water2 = (fx_Water2 * 1.43935*10^-4)*((4.217*9)*(4.217*9));
fy_Water2 = data_forces_Water2(:,3); Py_Water2 = (fy_Water2 * 1.43935*10^-4)*((4.217*9)*(4.217*9));
fz_Water2 = data_forces_Water2(:,4); Pz_Water2 = (fz_Water2 * 1.43935*10^-4)*((4.217*9)*(4.217*9));

timestep_Water2 = data_distance_Water2(:,1) * 2 * 10^-6 ; %ns
deltaZ_Water2 = data_distance_Water2(:,4); deltaZ_Water2 = deltaZ_Water2-2.5;

a=0;
for i = 1:1000:length(deltaZ_Water2)
    a=a+1;
    deltaz2_Water2(a) = mean(deltaZ_Water2(i):deltaZ_Water2(i)+999);
end

chdir('..')


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


timestep2_NW      = timestep_NW(1:1000:length(deltaZ_NW));
timestep2_Water1  = timestep_Water1(1:1000:length(deltaZ_Water1));
timestep2_Water2  = timestep_Water2(1:1000:length(deltaZ_Water2));

Pz2_NW      = Pz_NW(1:1000:length(deltaZ_NW));
Pz2_Water1  = Pz_Water1(1:1000:length(deltaZ_Water1));
Pz2_Water2  = Pz_Water2(1:1000:length(deltaZ_Water2));



figure(1)
hold on, box on
plot (deltaz2_NW-500, Pz2_NW)
plot (deltaz2_Water1-500, Pz2_Water1)
%plot (deltaz2_Water2-500, Pz2_Water2)
legend('No Water','With water 1', 'With Water 2')


figure(2)
hold on, box on
plot (deltaZ_NW, Pz_NW)
plot (deltaZ_Water1, Pz_Water1)
%plot (deltaZ_Water2, Pz_Water2)
legend('No Water','With water 1', 'With Water 2')

figure(3)
hold on, box on
plot (deltaZ_NW, Pz_NW)
plot (deltaZ_Water1, Pz_Water1)
legend('No Water','With water 1')
axis([0 30 -200 200])