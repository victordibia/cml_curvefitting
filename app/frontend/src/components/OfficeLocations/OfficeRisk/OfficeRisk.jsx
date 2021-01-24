import React, { useState } from "react";
import { Select } from "antd";
import sortBy from "lodash/sortBy";
import uniqBy from "lodash/uniqBy";
// import { loadJSONData } from "../../helperfunctions/HelperFunctions";
const { Option } = Select;

const OfficeRisk = (props) => {
  const locations = props.locations.map((x) => x.work_location);
  const trends = sortBy(
    props.trends.filter((x) => locations.includes(x.location)),
    "slope_data.slope"
  );

  // trends = trends;
  const [selectedLocation, setselectedLocation] = useState(0);
  const [showDetails, setShowDetails] = useState(false);
  const labels = uniqBy(
    trends.map((x) => x.slope_data.risk),
    (e) => e.color + e.label
  );

  const labelList = labels.map((data, i) => {
    const locs = trends.filter((x) => x.slope_data.risk.color === data.color);
    const locList = locs.map((data, i) => {
      return (
        <div className="text-sm" key={"locrow" + i}>
          <div
            className={
              "w-2.5 h-2.5 inline-block mr-2 " +
              "bg-" +
              data.slope_data.risk.color +
              "-500"
            }
          >
            {" "}
          </div>
          {data.location}{" "}
        </div>
      );
    });
    return (
      <div className="p3 flex-1  pr-3 " key={"labelrow" + i}>
        <div
          className={
            "p-1 pl-2 pr-2  whitespace-nowrap font-semibold rounded-sm mb-2 border " +
            "border-" +
            data.color +
            "-500"
          }
        >
          {" "}
          {data.label} ({locs.length})
        </div>
        {showDetails && <div>{locList}</div>}
      </div>
    );
  });

  const trendList = trends.map((data, i) => {
    return (
      <div className="text-sm" key={"locrow" + i}>
        <div
          className={
            "w-2.5 h-2.5 inline-block mr-2 " +
            "bg-" +
            data.slope_data.risk.color +
            "-500"
          }
        >
          {" "}
        </div>
        {data.location}{" "}
      </div>
    );
  });

  function clickShowMore(e) {
    setShowDetails(!showDetails);
  }
  return (
    trends.length > 0 && (
      <div className="riskdiv overflow-auto   mt-4 bg-white bg-opacity-90 rounded-sm  ">
        <div className=" inline-block    p-3 ">
          <div className="mb-2  flex">
            <span className="font-semibold flex-grow"> Office Risk</span>
            <span
              onClick={clickShowMore}
              className="text-xs mt-1 mr-3 hover:underline pb-1 cursor-pointer"
            >
              {" "}
              {showDetails ? "< Hide Details" : "Show Details > "}
            </span>
          </div>
          <div className="flex"> {labelList} </div>
          <div className="  overflow-auto"></div>
        </div>
      </div>
    )
  );
};

export default OfficeRisk;
