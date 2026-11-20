% =========================================
% SLAP BOT - MATLAB DATA ANALYSIS
% =========================================

clear;
clc;
close all;

% Load CSV data exported from Thonny
data = readmatrix('fsr_data.csv');

% Remove invalid rows
data = data(all(isfinite(data), 2), :);

% Extract data columns
time = data(:,1) / 1000;
face1 = data(:,2);
face2 = data(:,3);
chin = data(:,4);
score = data(:,5);

% Start time at zero
time = time - time(1);

% =========================================
% GRAPH 1 - SENSOR READINGS
% =========================================

figure('Name', 'Slap Bot Sensor Analysis');

subplot(2,1,1);

plot(time, face1, 'b', 'LineWidth', 1.5);
hold on;

plot(time, face2, 'g', 'LineWidth', 1.5);
plot(time, chin, 'r', 'LineWidth', 1.5);

hold off;

title('Slap Bot - FSR Sensor Responses');
xlabel('Time (seconds)');
ylabel('ADC Change from Baseline');

legend('Left Cheek', 'Right Cheek', 'Chin', ...
       'Location', 'best');

grid on;

% =========================================
% GRAPH 2 - SCORE
% =========================================

subplot(2,1,2);

plot(time, score, 'm', 'LineWidth', 2);

title('Slap Bot - Recorded Scores');
xlabel('Time (seconds)');
ylabel('Score');

grid on;

% =========================================
% STATISTICS
% =========================================

max_face1 = max(face1);
max_face2 = max(face2);
max_chin = max(chin);
max_score = max(score);

fprintf('\n===== SLAP BOT RESULTS =====\n');
fprintf('Peak Left Cheek: %.0f\n', max_face1);
fprintf('Peak Right Cheek: %.0f\n', max_face2);
fprintf('Peak Chin: %.0f\n', max_chin);
fprintf('Highest Score: %.0f\n', max_score);

% Save graph as image
exportgraphics(gcf, 'slapbot_graph.png', ...
               'Resolution', 300);
