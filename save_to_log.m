%% generate output save in the original order and not in the shuffeled order
% of trials
log = struct;
log.alignTimesScannerNames = {'t_scanner','t_scanner2','TimePoint1MRI','TimePoint2MRI'};
log.alignTimesScanner = [t_scanner,t_scanner2,TimePoint1MRI,TimePoint2MRI];
log.alignTimesETNames = {'TimePoint1ET','TimePoint2ET','status_AG_startTime1','status_AG_startTime2'}
log.alingTimesET = [TimePoint1ET,TimePoint2ET,status_AG_startTime1,status_AG_startTime2];
log.RT = RT;
log.randomValue = randomValue; %determine wich face will be worth 10 pnts and wich -10 pnts
log.pairs = pairs;
log.pairsValue = pairsValue;
log.reward = reward;
log.R = R;
log.R1 = R_ALL;
log.response = Response; %this holds the actual key press by the participant - left or right
log.subjectChoice = subjectChoice; % notice - this hold the choice with respect to the original faces order, and not the choice according to location on the screen!
log.correctResponse = correctResponse; % the correct respose that the participant should choose to maximize his point ( with respect to the original faces order, and not the choice according to location on the screen!) 1-left. 2 right, NaN - no correct response
log.correct = correct;
log.spatialLocations = allScreenOrder;
log.helpless = helpless;% 0-punshment vs. reward, 1-punshment vs. punishment, 2-rewars vs. reward
log.ExpTime = endTime - startTime;
log.faces = originals;
log.cumulativeReward = cumulativeReward;
log.shuffledTrialsOrder = shuffledTrialsOrder_ALL'; % The specific order of trials for this participant
log.originalOrder = originalOrder_ALL'; % The indices to put in the prameters to organize back in the original order ( [~, originalOrder] = sort(shuffledTrialsOrder) )
log.wrongKeyTrial = WrongKeyTrial;
log.wrongKeyPair = WrongKeyPair;
log.tooSlowTrial = TooSlowTrial;
log.tooSlowPair = TooSlowPair;
log.rewardMagnitude = RewardMagnitude;
log.positiveFace = find(ismember(randomValue,1));
log.neutralFace = find(ismember(randomValue,0));
log.negativeFace = find(ismember(randomValue,-1));
log.stimOnset = StimOnset;
log.rewardOnset = RewardOnset;
log.rectOnset = RectOnset;
log.fix1Onset = Fix1Onset;
log.fix2Onset = Fix2Onset;

if ~exist([logPath,num2str(sub_num)], 'dir')
    mkdir([logPath,num2str(sub_num)])
end

save([logPath,num2str(sub_num),'\learning_' num2str(sub_num) '_session_' num2str(session) '.mat'],'-struct','log');
save([logPath,num2str(sub_num), '\accumWinnings_' num2str(sub_num) '.mat'],'accumWinnings'); 

AG_EndTime = GetSecs;
if eyetracking %add to function
    status_endTime1 = Eyelink('Message', 'AG_EndTime');
    saveEDF(edfFile);
    Eyelink('Shutdown');
end