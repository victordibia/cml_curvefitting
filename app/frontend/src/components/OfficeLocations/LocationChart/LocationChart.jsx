import React, { useState } from "react";
import { Select } from "antd";
// import { loadJSONData } from "../../helperfunctions/HelperFunctions";
const { Option } = Select;

const LocationChart = (props) => {
  const locations = props.locations || [];
  const [selectedLocation, setselectedLocation] = useState(0);

  const workLocationList = locations.map((data, i) => {
    return (
      <Option value={data.work_location} key={"locrow" + i}>
        {" "}
        {data.work_location}{" "}
      </Option>
    );
  });
  return (
    <div>
      {locations.length > 0 && props.selectedLocation?.location && (
        <div className="mt-2   inline-block rounded-sm   bg-white p-3  bg-opacity-90">
          <div className="mb-2 text-sm font-semibold">
            {" "}
            Covid Trends for ({props.selectedLocation.location}){" "}
          </div>
          <div className="mb-2"> </div>
          Im the location Chart in D3
        </div>
      )}
    </div>
  );
};

export default LocationChart;
