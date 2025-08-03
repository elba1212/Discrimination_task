
%% Training - id this is the first discrimination session
% Show instructions
done_training =0;
while done_training == 0
    inst_training = imread([textPath, 'instructions_discrimination_MRI5.jpg']);
    Screen('PutImage', windowPtr, inst_training);
    Screen('Flip',windowPtr);
    KbWait([],2); %waits for a new key press
    
    WK = 1; %index for wrong key trials
    TS = 1; %index for too slow trials
    
    % trials loop
    trial=1;
    while trial<=numOfTrialsTraining
        % first screen show one morph
        morphNum = trial;
        morph = imread([trainingPath,num2str(morphNum),'.jpg']);
        textureIndex1 = Screen('MakeTexture', windowPtr, morph);
        Screen('DrawTexture', windowPtr, textureIndex1);%, [] ,[638.5 119 1281.5 762]);
        Screen('Flip', windowPtr);
        WaitSecs(1.5)
        
        % second screen - all the original and the participant need to choose
        % which one is the most similar to the morph he watched
        textureIndex = zeros(1,N);
        for s=1:N
            IM{s} = imread([trainingPath,'\originals\',num2str(Originals(s)),'.jpg']);
            textureIndex(1,s) = Screen('MakeTexture', windowPtr, IM{s});
        end
        
        hebWhichFig = [1489,1495,1512,47,1497,32,1489,1508,1512,1510,1493,1507,32,1492,1491,1493,1502,1492,32,1489,1497,1493,1514,1512,32,1500,1508,1512,1510,1493,1507,32,1492,1511,1493,1491,1501];
        if flipText=='y'
            hebWhichFig=flip(hebWhichFig);
        end
        DrawFormattedText(windowPtr, hebWhichFig,'center',(screenYpixels/5),[255 255 255]);
        Screen('DrawTextures', windowPtr, textureIndex, [] ,locationN');
        [~, StimOnset] = Screen('Flip', windowPtr); % dontClear flag is set to 1 to overdraw the frame on the figure
        PsychHID('KbQueueFlush',[], 3); %Flushes all scored and unscored keyboard events from a queue.
        [event,~] = PsychHID('KbQueueGetEvent',[],3); % collect response - Max 3 seconds%
        
        % check the response
        if ~isempty(event)
            keypress = event.Keycode;
            switch keypress
                case leftKey %left arrow
                    Response_training(trial) =  1;
                    RT_training(trial) = event.Time-StimOnset;
                    Screen('DrawTextures', windowPtr, textureIndex, [] ,locationN');
                    Screen('FrameRect',windowPtr,[237 177 32],locationN(1,:),8)
                    Screen('Flip', windowPtr);
                    WaitSecs(0.2) % 200 ms in addition to the 500 ms at the end of the trial
                    trial=trial+1;
                    
                case downKey %down arrow
                    Response_training(trial) =  2;
                    RT_training(trial) = event.Time-StimOnset;
                    Screen('DrawTextures', windowPtr, textureIndex, [] ,locationN');
                    Screen('FrameRect',windowPtr,[237 177 32],locationN(2,:),8)
                    Screen('Flip', windowPtr);
                    WaitSecs(0.2) % 200 ms in addition to the 500 ms at the end of the trial
                    trial=trial+1;
               
                case rightKey % right arrow
                    Response_training(trial) =  3;
                    RT_training(trial) = event.Time-StimOnset;
                    Screen('DrawTextures', windowPtr, textureIndex, [] ,locationN');
                    Screen('FrameRect',windowPtr,[237 177 32],locationN(3,:),8)
                    Screen('Flip', windowPtr);
                    WaitSecs(0.2) % 200 ms in addition to the 500 ms at the end of the trial
                    trial=trial+1;
               
                case escapeKey % Esc
                    PsychHID('KbQueueFlush',[], 3); %Flushes all scored and unscored keyboard events from a queue.
                    PsychHID('KbQueueRelease');
                    Screen('CloseAll')
                    break;
                otherwise
                    wrongKey = [1502,1511,1513,32,1513,1490,1493,1497,32];
                    if flipText=='y'
                         wrongKey=flip(wrongKey);
                    end
                    DrawFormattedText(windowPtr, wrongKey,'center','center',[255 255 255]);
                    Screen('Flip', windowPtr);
                    WrongKeyTrial_training(WK) = trial;
                    WrongKeyMorph_training(WK) = morphNum;
                    WK=WK+1;
            end
            
        else %no response
            tooSlow = [1504,1490,1502,1512,32,1492,1494,1502,1503,32];
            if flipText=='y'
                tooSlow=flip(tooSlow);
            end
            DrawFormattedText(windowPtr, tooSlow,'center','center',[255 255 255]);
            Screen('Flip', windowPtr);
            TooSlowTrial_training(TS) = trial;
            TooSlowMorph_training(TS) = morphNum;
            TS=TS+1;
            
            
        end
        
        WaitSecs(0.5)
    end
    
    %end of training
    end_training = imread([textPath, 'training_end_dis.jpg']);
    Screen('PutImage', windowPtr, end_training);
    Screen('Flip',windowPtr);
    pause(1)
    

        PsychHID('KbQueueFlush',[], 3); %Flushes all scored and unscored keyboard events from a queue.
        [event,~] = PsychHID('KbQueueGetEvent',[],300); % collect response - Max 300 seconds%
        if ~isempty(event)
            keyPressed = event.Keycode;
            switch keyPressed
                case leftKey
                     done_training = 1;
                case rightKey
                    done_training = 0;
                case escapeKey
                    PsychHID('KbQueueFlush',[], 3); %Flushes all scored and unscored keyboard events from a queue.
                    PsychHID('KbQueueRelease');
                    Screen('CloseAll')
                    break;
            end
        end
        
    
end