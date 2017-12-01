package net.solarquant.neuralnet;

import java.io.File;

import net.solarquant.database.DBHandler;
import net.solarquant.database.RequestData;
import net.solarquant.util.StatusEnum;



/**
 * Training Manager class first tests if the oldest training process has completed.
 * After this, it proceeds to start a new one in the inital state if it exists.
 * @author matthew
 *
 */
public class TrainingManager extends NetManager{

	private DBHandler db = new DBHandler();	
	private static final String TRAINING_TABLE = "training_requests";

	@Override
	public void manageJobs() {

		RequestData rd = db.getOldestRequest(TRAINING_TABLE , StatusEnum.RUNNING);

		int reqId = rd.getRequestId();
		String engine = rd.getEngineName();
		
		if(rd != null) {
			if(hasTrainingRunComplete(reqId, engine)) {
				db.updateRequestStatus(TRAINING_TABLE, reqId);			
			}else {
				return;
			}
		}
		
		rd = db.getOldestRequest(TRAINING_TABLE, StatusEnum.INITIAL);
		if(rd != null) {
			
			reqId = rd.getRequestId();
			engine = rd.getEngineName();

			startTraining(reqId, engine);
			db.updateRequestStatus(TRAINING_TABLE, reqId);

		}else {
			return;
		}

	}



	private boolean hasTrainingRunComplete(int requestId, String engine) {		
		if(new File("../tensorflow/SolarQuant/trained_models/"+requestId+"_model.h5").exists()) {
			return true;
		}		
		return false;	
	}

	private void startTraining(int requestId, String engine) {
		Runtime.getRuntime().exec("");



	}

}
