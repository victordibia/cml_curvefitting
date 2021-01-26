import React, { useState } from "react";
import { Select } from "antd";
// import { loadJSONData } from "../../helperfunctions/HelperFunctions";
const { Option } = Select;
const OfficeSelector = (props) => {
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
    locations.length > 0 && (
      <div className="mt-2   inline-block rounded-sm   bg-white p-3  bg-opacity-90">
        <div className="mb-2 text-sm font-semibold">
          {" "}
          Location Type ({locations.length}){" "}
        </div>
        <div className="mb-2"> </div>
        {/* <Select
          defaultValue={locations[selectedLocation].work_location}
          showSearch
          style={{ width: 200 }}
          placeholder="Select a location"
          optionFilterProp="children"
          // onChange={onChange}
          // onFocus={onFocus}
          // onBlur={onBlur}
          // onSearch={onSearch}
          filterOption={(input, option) =>
            option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
          }
        >
          {workLocationList}
        </Select> */}

        <div className="mt-2">
          <Select
            defaultValue={props.locationType}
            showSearch
            style={{ width: 200 }}
            placeholder="Select a location"
            optionFilterProp="children"
            onChange={(e) => {
              props.setLocationType(e);
            }}
            // onFocus={onFocus}
            // onBlur={onBlur}
            // onSearch={onSearch}
            filterOption={(input, option) =>
              option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
            }
          >
            <Option value="work">Work Locations</Option>
            <Option value="all">All Employee Locations</Option>
          </Select>
          <div className="text-xs mt-1 text-gray-500">
            {" "}
            Data last updated 2 days ago.
          </div>
        </div>
      </div>
    )
  );
};

export default OfficeSelector;
