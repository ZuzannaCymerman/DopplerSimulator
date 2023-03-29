load("dsss_m4_B8000_data3_ks5.mat")
a =out(1:96000).';
T = array2table(a)
T.Properties.VariableNames(1:1) = {'data'}
writetable(T,"dsss_m4_B8000_data3_ks5_0_1s.csv")
% csvwrite("dsss_m4_B8000_data3_ks5_0_1s.csv","data")
% writematrix(a,"dsss_m4_B8000_data3_ks5_0_1s.csv")


% load("dsss_m4_B5000_data3_ks5.mat")
% writematrix(out,'dsss_m4_B5000_data3_ks5.csv') 
% 
% load("dsss_m4_B4000_data3_ks5.mat")
% writematrix(out,'dsss_m4_B4000_data3_ks5.csv') 
% 
% load("dsss_m4_B2500_data3_ks5.mat")
% writematrix(out,'dsss_m4_B2500_data3_ks5.csv') 