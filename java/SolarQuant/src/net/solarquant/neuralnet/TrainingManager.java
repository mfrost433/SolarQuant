package net.solarquant.neuralnet;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URISyntaxException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Properties;

import org.apache.commons.lang.time.DateUtils;
import org.apache.log4j.BasicConfigurator;
import org.apache.log4j.Logger;
import org.apache.log4j.Priority;
import org.apache.log4j.PropertyConfigurator;

import net.solarquant.database.DBHandler;
import net.solarquant.database.Request;
import net.solarquant.res.Resource;
import net.solarquant.util.StatusEnum;


/**
 * Training Manager class first tests if the oldest training process has completed.
 * After this, it proceeds to start a new one in the inital state if it exists.
 * @author matthew
 *
 */
public class TrainingManager extends NetManager{
	
	private Logger logger = Logger.getLogger(TrainingManager.class);
	private String location;
	private DBHandler db = new DBHandler();	
	private static final String TRAINING_TABLE = "training_requests";

	public TrainingManager() {

		InputStream log4jConf = Resource.class.getResourceAsStream("log4j.properties");
        Properties prop = new Properties();
        try {
			prop.load(log4jConf);
			PropertyConfigurator.configure(prop);
			logger.info("Training Manager started");
		} catch (IOException e) {
			logger.error("ERROR:",e);
		}

		try {
			location = new File(TrainingManager.class.getProtectionDomain().
					getCodeSource().getLocation().toURI().getPath()).getParent();

		} catch (URISyntaxException e) {
			logger.error("ERROR:",e);
		}
	}
	@Override
	public void manageJobs() {
		int reqId;
		String engine;
		
		//First check for running jobs - highest priority
		logger.info("Checking running jobs...");
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
		logger.info("Checking data retrieval jobs...");
		rd = db.getOldestRequest(TRAINING_TABLE, StatusEnum.RETRIEVING_DATA);
		if(rd != null) {

			if(verifyStoredData(rd)) {
				logger.info("Stored data verified up to date.");
				reqId = rd.getRequestId();
				engine = rd.getEngineName();
				logger.info("Starting training");
				boolean success = startTraining(reqId, engine);

				if(success) {
					logger.info("Successfully started training");
					rd.updateStatus(StatusEnum.RUNNING);
					return;
				}
			}else {
				return;
			}
		}

		//next check for jobs in initial state to progress
		logger.info("Checking inital state jobs...");
		rd = db.getOldestRequest(TRAINING_TABLE, StatusEnum.INITIAL);
		if(rd != null) {
			if(!verifyStoredData(rd)) {
				updateStoredData(rd);
				logger.info("Begun retrieving data.");
				rd.updateStatus(StatusEnum.RETRIEVING_DATA);				
				return;

			}else {
				logger.info("Stored data verified up to date.");
				reqId = rd.getRequestId();
				engine = rd.getEngineName();
				logger.info("Starting training");
				boolean success = startTraining(reqId, engine);

				if(success) {
					logger.info("Successfully started training");
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

		ProcessBuilder pb;		
		if(lastDate == null) {
			//if is first time retrieving data for this node/source, do not set start/end parameters
			pb = new ProcessBuilder("python", "DatabasePopulator.py", "-r", ""+r.getRequestId());

		}else {

			String start = new SimpleDateFormat("yyyy-M-dd").format(lastDate);
			String end = new SimpleDateFormat("yyyy-M-dd").format(cDate);

			pb = new ProcessBuilder("python", "DatabasePopulator.py", "-r", ""+r.getRequestId(), "-s", start, "-e", end);
		}
		pb.directory(new File(location+"/../../data_retrieval"));
		logger.info("running data retrieval python at location: "+location+"/../../data_retrieval");

		try {

			Process p = pb.start();
			
			/*
			InputStream i = p.getInputStream();
			InputStream e = p.getErrorStream();
			InputStreamReader ir = new InputStreamReader(e);
			BufferedReader b = new BufferedReader(ir);
			String l;
			while((l=b.readLine())!= null){
				System.out.println(l);
			}
			*/

		} catch (IOException e) {
			logger.error("ERROR:",e);
		}
	}

	private boolean hasTrainingRunComplete(int requestId, String engine) {

		System.out.println(new File(location+"/../../tensorflow/SolarQuant/src/trained_models/"+requestId+"_model.h5").exists());
		if(new File(location+"/../../tensorflow/SolarQuant/src/trained_models/"+requestId+"_model.h5").exists()) {
			return true;
		}		
		return false;	
	}

	private boolean startTraining(int requestId, String engine) {

		if(engine.equalsIgnoreCase("tensorflow")) {

			ProcessBuilder pb = new ProcessBuilder("python", "QuantExecutor.py", "-r", ""+requestId);
			pb.directory(new File(location + "/../../tensorflow/SolarQuant/src/"));

			try {
				Process p = pb.start();
				InputStream i = p.getInputStream();
				InputStream e = p.getErrorStream();
				InputStreamReader ir = new InputStreamReader(e);
				BufferedReader b = new BufferedReader(ir);
				String l;
				while((l=b.readLine())!= null){
					System.out.println(l);
				}

			} catch (IOException e) {
				logger.error("ERROR:",e);
				return false;

			}

		}

		return true;
	}


}
