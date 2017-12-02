package net.solarquant.neuralnet;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import org.apache.commons.lang.time.DateUtils;
import net.solarquant.database.DBHandler;
import net.solarquant.database.Request;
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
		int reqId;
		String engine;

		//First check for running jobs - highest priority
		Request rd = db.getOldestRequest(TRAINING_TABLE , StatusEnum.RUNNING);
		if(rd != null) {
			reqId = rd.getRequestId();
			engine = rd.getEngineName();
			if(hasTrainingRunComplete(reqId, engine)) {
				rd.updateStatus(StatusEnum.FINISHED);
			}else {
				return;
			}
		}

		//Next check for requests that are in retrieving data state.
		rd = db.getOldestRequest(TRAINING_TABLE, StatusEnum.RETRIEVING_DATA);
		if(rd != null) {

			if(verifyStoredData(rd)) {

				reqId = rd.getRequestId();
				engine = rd.getEngineName();
				boolean success = startTraining(reqId, engine);

				if(success) {
					rd.updateStatus(StatusEnum.RUNNING);
				}
			}else {
				return;
			}
		}

		//next check for jobs in initial state to progress
		rd = db.getOldestRequest(TRAINING_TABLE, StatusEnum.INITIAL);
		if(rd != null) {

			if(!verifyStoredData(rd)) {
				updateStoredData(rd);
				rd.updateStatus(StatusEnum.RETRIEVING_DATA);				
				return;

			}else {

				reqId = rd.getRequestId();
				engine = rd.getEngineName();
				boolean success = startTraining(reqId, engine);

				if(success) {
					rd.updateStatus(StatusEnum.RUNNING);
				}
			}

		}else {
			return;
		}

	}
	//checks if stored data is up to date with the current day's datum
	private boolean verifyStoredData(Request r) {
		Date lastDate = db.getLatestTrainingDataDate(r);
		System.out.println(lastDate);
		if(lastDate == null) {
			return false;
		}
		Date cDate = new Date();

		if(DateUtils.isSameDay(lastDate, cDate)) {
			return true;
		}else {
			return false;
		}

	}
	//returns true if the data is already up to date, else sets process to start downloading and exits.
	private void updateStoredData(Request r) {

		Date lastDate = db.getLatestTrainingDataDate(r);
		Date cDate = new Date();
		if(lastDate == null) {
			try {
				lastDate = new SimpleDateFormat("yyyy-M-dd").parse("2016-1-01");
			} catch (ParseException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		String command = "python com/database/DatabasePopulator.py -n %s -i %s -s %s -e %s";

		String start = new SimpleDateFormat("yyyy-M-dd").format(lastDate);
		String end = new SimpleDateFormat("yyyy-M-dd").format(cDate);

		command = String.format(command, r.getNodeId(), r.getSourceId(), start, end);
		System.out.println(command);
		ProcessBuilder pb = new ProcessBuilder("python", "DatabasePopulator.py", "-n", ""+r.getNodeId()
		, "-i", r.getSourceId(), "-s", start, "-e", end);
		pb.directory(new File("../../data_retrieval"));

		try {

			Process p = pb.start();

		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	private boolean hasTrainingRunComplete(int requestId, String engine) {

		System.out.println(new File("../../tensorflow/SolarQuant/src/trained_models/"+requestId+"_model.h5").exists());
		if(new File("../../tensorflow/SolarQuant/src/trained_models/"+requestId+"_model.h5").exists()) {
			return true;
		}		
		return false;	
	}

	private boolean startTraining(int requestId, String engine) {

		if(engine.equalsIgnoreCase("tensorflow")) {

			ProcessBuilder pb = new ProcessBuilder("python", "QuantExecutor.py", "-r", ""+requestId);
			pb.directory(new File("../../tensorflow/SolarQuant/src/"));

			try {
				Process p = pb.start();
				/*
				InputStream i = p.getInputStream();
				InputStreamReader ir = new InputStreamReader(i);
				BufferedReader b = new BufferedReader(ir);
				String l;
				while((l = b.readLine()) != null) {
					System.out.println(l);
				}
				*/
			} catch (IOException e) {
				e.printStackTrace();
				return false;

			}

		}

		return true;
	}


}
