import React, { useEffect } from "react";
import { Select } from "antd";
import { loadJSONData } from "../../helperfunctions/HelperFunctions";
import "./officeselector.css";

const { Option } = Select;
const OfficeSelector = () => {
  return (
    <div className=" hover:bg-opacity-40 bg-opacity-20 bg-gray-500 p-3 h-full">
      <div className="mb-2 text-sm"> Office Selector </div>
      <Select
        defaultValue={"US Brooklyn New York"}
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
        <Option value="jack" selected>
          US Brooklyn New York
        </Option>
        <Option value="lucy">US Santa Clara California</Option>
        <Option value="tom">Tom</Option>
      </Select>
    </div>
  );
};

export default OfficeSelector;
