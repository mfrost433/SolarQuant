package net.solarquant.main;


import net.solarquant.neuralnet.PredictionManager;
import net.solarquant.neuralnet.TrainingManager;

public class Main {

	public static void main(String[] args) {
		
		new TrainingManager().manageJobs();
		new PredictionManager().manageJobs();
		
		
	}
	
}
