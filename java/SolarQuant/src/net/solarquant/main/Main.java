package net.solarquant.main;


import net.solarquant.neuralnet.EmergentTrainingManager;
import net.solarquant.neuralnet.PredictionManager;
import net.solarquant.neuralnet.TensorflowPredictionManager;
import net.solarquant.neuralnet.TensorflowTrainingManager;
import net.solarquant.neuralnet.TrainingManager;

public class Main {

	public static void main(String[] args) {

		new TensorflowTrainingManager().manageJobs();
		new EmergentTrainingManager().manageJobs();
		new TensorflowPredictionManager().manageJobs();
		
		
		
	}
	
}
