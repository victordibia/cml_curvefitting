import React, { useEffect, useState } from "react";
import { Select } from "antd";
import * as d3 from "d3";
// import { loadJSONData } from "../../helperfunctions/HelperFunctions";
const { Option } = Select;

const LocationChart = (props) => {
  const locations = props.locations || [];
  const uncertaintyColor = "rgba(147, 197, 253,0.3)";
  const trendColor = "rgba(245, 158, 11,1)";
  const dataColor = "rgba(107, 114, 128, 0.8)";
  // const [selectedLocation, setselectedLocation] = useState(0);
  // console.log(props.trends);
  const animDuration = 100;
  const minChartWidth = 350;
  const minChartHeight = 150;
  const chartMargin = { top: 10, right: 5, bottom: 25, left: 20 };
  const chartWidth = minChartWidth - chartMargin.left - chartMargin.right;
  const chartHeight = minChartHeight - chartMargin.top - chartMargin.bottom;

  let x, y, xAxis, yAxis;
  const line = d3
    .line()
    .x(function (d, i) {
      return x(i);
    })
    .y(function (d) {
      return y(d);
    });
  // set the y values for the line generator
  // .curve(d3.curveMonotoneX) // apply smoothing to the line

  const msearea = d3
    .area()
    .x(function (d, i) {
      return x(i);
    })
    .y0(function (d) {
      return y(d[0]);
    })
    .y1(function (d) {
      return y(d[1]);
    });

  const selectedTrend = props.trends.filter(
    (x) => x.location === props.selectedLocation.location
  )[0];

  const workLocationList = locations.map((data, i) => {
    return (
      <Option value={data.work_location} key={"locrow" + i}>
        {" "}
        {data.work_location}{" "}
      </Option>
    );
  });

  function setupScalesAxes(data) {
    var n = data.length;

    x = d3
      .scaleLinear()
      .domain([0, n - 1]) // input
      .range([0, chartWidth]); // output

    y = d3
      .scaleLinear()
      .domain([d3.min(data), d3.max(data)]) // input
      .range([chartHeight, 0]); // output

    xAxis = d3.axisBottom(x);
    yAxis = d3.axisRight(y).tickSize(minChartWidth);
  }

  useEffect(() => {
    drawChart();
  }, []);

  useEffect(() => {
    updateChart();
  }, [props.selectedLocation]);

  function updateChart() {
    // console.log(d3.select("div.linechartbox"));
    const data = selectedTrend?.data || [];
    const trendData = selectedTrend?.trend_pred || [];
    const trendUpperData = selectedTrend?.trend_pred_upper || [];
    const trendLowerData = selectedTrend?.trend_pred_lower || [];

    const trendAreaData = trendUpperData.map((x, i) => {
      return [x, trendLowerData[i]];
    });

    setupScalesAxes(data);
    var svg = d3.select("div.linechartbox").transition();

    svg
      .select(".dataline") // change the input line
      .duration(animDuration)
      .attr("stroke", "gray")
      .attr("fill", "none")
      .attr("d", line(data));

    svg
      .select(".trendline") // change the input line
      .duration(450)
      .attr("stroke", "orange")
      .attr("fill", "none")
      .attr("d", line(trendData));

    svg
      .select(".msearea")
      .duration(animDuration)
      .attr("fill", uncertaintyColor)
      .attr("stroke", "none")
      .attr("d", msearea(trendAreaData));
  }

  function drawChart() {
    const data = selectedTrend?.data || [];
    const trendData = selectedTrend?.trend_pred || [];
    const trendUpperData = selectedTrend?.trend_pred_upper || [];
    const trendLowerData = selectedTrend?.trend_pred_lower || [];
    const trendAreaData = trendUpperData.map((x, i) => {
      return [x, trendLowerData[i]];
    });
    setupScalesAxes(data);

    const width = chartWidth,
      height = chartHeight,
      margin = chartMargin;

    // 7. d3's line generator

    const svg = d3
      .select("div.linechartbox")
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg
      .append("path")
      .datum(data) // 10. Binds data to the line
      .attr("class", "dataline") // Assign a class for styling
      .attr("stroke", "grey")
      .attr("stroke-width", 1.5)
      .attr("fill", "none")
      .attr("d", line); // 11. Calls the line generator

    svg
      .append("path")
      .datum(trendData) // 10. Binds data to the line
      .attr("class", "trendline") // Assign a class for styling
      .attr("stroke", "green")
      .attr("fill", "none")
      .attr("stroke-width", 1.5)
      // .attr("opacity", 1)
      .attr("d", line); // 11. Calls the line generator

    svg
      .append("path")
      .datum(trendAreaData)
      .attr("class", "msearea") // Assign a class for styling
      .attr("fill", uncertaintyColor)
      .attr("stroke", "none")
      .attr("d", msearea);
  }

  const isLocationsLoaded = locations.length > 0;
  const isLocationSelected = props.selectedLocation?.location;

  return (
    <div>
      {
        <div
          className={
            "mt-2   inline-block rounded-sm   bg-white p-3  bg-opacity-90 " +
            (isLocationsLoaded && isLocationSelected ? "" : " hidden")
          }
        >
          <div className="mb-2 text-sm font-semibold">
            {" "}
            Covid Trends for ({props.selectedLocation.location}){" "}
          </div>

          <div id="linechartbox" className="linechartbox"></div>
          <div>
            <span className="w-2 h-2 bg-gray-500 inline-block"> </span>{" "}
            <span className="text-sm mr-3"> data </span>
            <span className="w-2 h-2 bg-yellow-600 inline-block"> </span>{" "}
            <span className="text-sm mr-3"> trend </span>
            <span className="w-2 h-2 bg-blue-300 inline-block"> </span>{" "}
            <span className="text-sm"> uncertainty </span>
          </div>
        </div>
      }
    </div>
  );
};

export default LocationChart;
