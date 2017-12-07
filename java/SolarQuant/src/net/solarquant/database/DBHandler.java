
package net.solarquant.database;

import java.sql.Connection;
import java.sql.Date;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import net.solarquant.util.StatusEnum;

/**
 * 
 * Database handler class contains specific methods relating to request data and state.
 * 
 * <p>TODO </p>
 * 
 * @author matthew
 * @version 1.0
 */
public class DBHandler {

	private static final String CONNECTION_STRING = "jdbc:mysql://localhost/solarquant?"
			+ "user=solarquant&password=solarquant";

	private Connection conn_;

	public DBHandler() {
		getConnection();
	}

	private void getConnection() {
		try {
			conn_ = DriverManager.getConnection(CONNECTION_STRING);
		} catch ( SQLException ex ) {
			System.out.println("SQLException: " + ex.getMessage());
		}
	}

	// gets the oldest request, as the requests are processed in LIFO queue
	public Request getOldestRequest(String tableName, StatusEnum status) {
		Statement stmt = null;
		try {
			String query = "SELECT * FROM %s WHERE STATUS = %s " + "ORDER BY DATE_REQUESTED ASC LIMIT 1";
			query = String.format(query, tableName, status.getStateId(), tableName);
			stmt = conn_.createStatement();
			ResultSet rs = stmt.executeQuery(query);

			if ( rs.next() == false ) {
				return null;
			} else {
				return new Request(rs.getDate("DATE_REQUESTED"), rs.getString("REQUEST_ENGINE"),
						rs.getInt("STATUS"), rs.getInt("REQUEST_ID"), rs.getInt("NODE_ID"),
						rs.getString("SOURCE_ID"));
			}

		} catch ( SQLException e ) {
			e.printStackTrace();
		}
		return null;

	}

	//changes the current status to the new status specified in input
	public void updateRequestStatus(String tableName, int reqId, int newStatus) {
		Statement stmt = null;
		try {
			String query = "UPDATE %s SET STATUS = " + newStatus + " WHERE REQUEST_ID = %s";
			query = String.format(query, tableName, reqId);
			stmt = conn_.createStatement();
			stmt.execute(query);

		} catch ( SQLException e ) {
			e.printStackTrace();
		}
	}
	// gets the most recent date for the addition of new data for a specific node+source
	// prevents the unnecessary downloading of existing data
	public Date getLatestTrainingDataDate(Request r) {
		String query = "SELECT ENTRY_DATE FROM %s WHERE NODE_ID = %s AND SOURCE_ID = '%s' "
				+ "ORDER BY ENTRY_DATE DESC LIMIT 1";

		if ( r.getEngineName().equalsIgnoreCase("tensorflow") ) {
			query = String.format(query, "tensorflow_training_input", r.getNodeId(), r.getSourceId());
		}

		Statement stmt;
		try {
			stmt = conn_.createStatement();
			ResultSet rs = stmt.executeQuery(query);

			if ( rs.next() == true ) {
				Date out = rs.getDate("ENTRY_DATE");
				return out;
			} else {
				return null;
			}

		} catch ( SQLException e ) {
			e.printStackTrace();
			return null;
		}

	}
}
