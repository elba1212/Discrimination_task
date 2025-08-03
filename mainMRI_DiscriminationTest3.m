% This script is the experimental structure for the Discrimination Test.
% 1. Define  
% 2. Gets subject number
% 3. calls the discrimination test function
% 4. sav
    


% Default settings for setting up Psychtoolbox
flag1=1;
while flag1 %the flag is for breaking if the file is already exit
     



    % Default settings for setting up Psychtoolbox 


    
    PsychDefaultSetup(2);
    Screen('Preference', 'VisualDebugLevel',1); %tp avoid showin the psychtoolbox logo at the first screen
    Screen('Preference', 'SkipSyncTests', 2); %skips the synchroniztion test to bypass errors
    % debug mode - transparewnt  
    %PsychDebugWindowConfiguration;
    % set paths
    pathsLearningFaces

    % Get Subject Number and Session number
    prompt = {'Subject number: ','Session ',' Men/Women faces (m/w):', 'Flip hebrew text (y/n)', 'Training (y/n)'};
    dlgtitle = 'Input';
    dims = [1 60];
    definput = {'999','1','m','y','y'};
    subject_input_information = inputdlg(prompt,dlgtitle,dims,definput);
    sub_num = str2double(subject_input_information{1});
    session = str2double(subject_input_information{2});
    MWfaces = subject_input_information{3}; % choose men or women faces stimuli (m/w)
    flipText = (subject_input_information{4}); % for some computers the hebrew text is fliped to flip it back set this value to 1
    training = (subject_input_information{5}); % check whether there is a need for training


    if isfile([logPath,num2str(sub_num),'\discriminationTest_' num2str(sub_num) '_session_' num2str(session) '.mat'])
        prompt = {'the file is already exist. Do you want to overwrite: (y/n)'}
        dlgtitle = 'Input';
        dims = [1 60];
        definput = {'n'};
        subject_input_information = inputdlg(prompt,dlgtitle,dims,definput);
        if subject_input_information{1}~='y'
            flag1=0;
            break
        end
    end

    if session==2
        prompt = {'please enter the accumWinnings from the learning task:'};
        dlgtitle = 'Input';
        dims = [1 60];
        subject_input_information = inputdlg(prompt,dlgtitle,dims);
        accumWinnings=str2double(subject_input_information);
    elseif session==3
        accumWinnings = load([logPath,num2str(sub_num),'\accumWinnings_' num2str(sub_num) '.mat']);
        accumWinnings = accumWinnings.accumWinnings;
    end


    % Experiment parameters:
    % number of original faces4
    N=3;
    faces=1:N;
    % which faces are the originals
    if session>1
        log1 = load ([logPath,num2str(sub_num),'\discriminationTest_',num2str(sub_num) '_session_1.mat']);
        Originals = log1.faces;
    elseif session==1 % first session

        % random the order between the faces
        Originals = randsample(faces,N);

        accumWinnings = 0;
    else
        error('Error. wrong session number.')
    end
    % number of morphs on the axis
    nMorphs = 66;
    %number of repetitions
    Repetitions = 6;
    %instructions
    Instructions = {'instructions_discrimination_MRI1', 'instructions_discrimination_MRI2', 'instructions_discrimination_MRI3', 'instructions_discrimination_MRI4'};
    %Reward Magnitude
    RewardMagnitude = 1;

    morphs_division(1,:) = [1	12	2	22	13	3	31	23	14	4	39	32	24	15	5	40	33	25	16	34]; %all the morphs associated with original face 1
    morphs_division(2,:) = [11	21	10	30	20	9	38	29	19	8	45	37	28	18	7	44	36	27	17	35]; %all the morphs associated with original face 2
    morphs_division(3,:) = [66	64	65	61	62	63	57	58	59	60	52	53	54	55	56	47	48	49	50	42]; %all the morphs associated with original face 3


    %% The test exit
    [log, accumWinnings] = facesDiscriminationTest3(MWfaces,Originals, nMorphs, N,morphs_division, Repetitions, Instructions,RewardMagnitude, accumWinnings,flipText,training);
    Screen('CloseAll')
    %% save parameters
    if session==1
        mkdir([logPath,num2str(sub_num)])
    end
    save([logPath,num2str(sub_num),'\discriminationTest_',num2str(sub_num) '_session_' num2str(session) '.mat'],'-struct','log');
    save([logPath,num2str(sub_num),'\accumWinnings_' num2str(sub_num) '.mat'],'accumWinnings');

    flag1=0
end
