
package net.solarquant.database;

import java.sql.Date;
import net.solarquant.util.StatusEnum;

/**
 * This class represents a user request for training or predictions, and
 * encapsulates the data, and allows for status updates
 * 
 * @author matthew
 *
 */
public class Request {

	private DBHandler d = new DBHandler();

	private Date date_;
	private String engine_;
	private StatusEnum status_;
	private int requestId_, nodeId_;
	private String sourceId_;

	public Request(Date date, String engine, int status, int requestId, int nodeId, String sourceId) {

		date_ = date;
		engine_ = engine;
		status_ = StatusEnum.fromInt(status);
		requestId_ = requestId;
		nodeId_ = nodeId;
		sourceId_ = sourceId;

	}

	public Date getRequestDate() {
		return date_;
	}

	public String getEngineName() {
		return engine_;
	}

	public StatusEnum getStatus() {
		return status_;
	}

	public int getRequestId() {
		return requestId_;
	}

	public int getNodeId() {
		return nodeId_;
	}

	public String getSourceId() {
		return sourceId_;
	}

	public void updateStatus(StatusEnum newStatus) {

		d.updateRequestStatus("training_requests", requestId_, newStatus.getStateId());

	}

}
