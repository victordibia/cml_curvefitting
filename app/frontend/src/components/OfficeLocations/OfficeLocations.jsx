import React, { useEffect, useState } from "react";
import "./officelocation.css";

import DeckGL from "@deck.gl/react";
import { ScatterplotLayer, LineLayer, ArcLayer } from "@deck.gl/layers";
import { HeatmapLayer } from "@deck.gl/aggregation-layers";
import { StaticMap } from "react-map-gl";
import { MapView } from "@deck.gl/core";
import OfficeSelector from "./OfficeSelector/OfficeSelector";
import LocationChart from "./LocationChart/LocationChart";
import { Popover } from "antd";

import { loadJSONData, textToRGB } from "../helperfunctions/HelperFunctions";
import OfficeRisk from "./OfficeRisk/OfficeRisk";

// Set your mapbox access token here
const MAPBOX_ACCESS_TOKEN = process.env.REACT_APP_MAPBOX_TOKEN;

const OfficeLocations = (props) => {
  const [locations, setLocations] = useState({ work: [], all: [] });
  const [trends, setTrends] = useState([]);
  const [locationType, setLocationType] = useState("work");
  const [selectedLocation, setSelectedLocation] = useState({});

  // Viewport settings

  const INITIAL_VIEW_STATE = {
    longitude: 18.419257623928356,
    latitude: 47.22416217215195,
    zoom: 1.3,
    pitch: 10,
    bearing: 0,
  };

  let trendsDictionary = {};
  trends.forEach((x) => {
    trendsDictionary[x.location] = x.slope_data.risk;
  });

  const santaClara =
    locations[locationType].filter((x) =>
      x.work_location.includes("Santa Clara")
    )[0] || {};

  const santaClaraRisk = trendsDictionary["US-California-Santa Clara (HQ)"];
  const santaClaraLatLong = [santaClara.geo_long, santaClara.geo_lat];
  // Data to be used by the LineLayer
  const lineData = [
    {
      sourcePosition: [-121.9552356, 37.3541079],
      targetPosition: [-122.41669, 37.781],
    },
  ];

  // console.log(locations[locationType]);
  let connectionData = [];
  let locationCordinates = [];
  locations[locationType].forEach((x) => {
    const targetPosition = [x.geo_long, x.geo_lat];
    connectionData.push({
      sourcePosition: santaClaraLatLong,
      targetPosition: targetPosition,
      sourceRisk: santaClaraRisk,
      targetRisk: trendsDictionary[x.work_location],
    });

    locationCordinates.push({
      coords: targetPosition,
      risk: trendsDictionary[x.work_location],
      location: x.work_location,
    });
  });

  const locationsData = [
    [-121.9552356, 37.35410793],
    [-122.41669, 37.781],
  ];

  useEffect(() => {
    const trendsPath = props.selections.serverBasePath + "/trends";
    const locationsPath = props.selections.serverBasePath + "/locations";
    console.log("Trends and Locations Data requested ..");

    let locPromise = loadJSONData(locationsPath);
    locPromise
      .then(function (data) {
        if (data) {
          setLocations(data);
        }
      })
      .catch(function (err) {
        console.log("Failed to fetch locations data.", err);
      });

    let trendPromise = loadJSONData(trendsPath);
    trendPromise
      .then(function (data) {
        if (data) {
          setTrends(data);
        }
      })
      .catch(function (err) {
        console.log("Failed to fetch trends data.", err);
      });
  }, [props.selections.serverBasePath]);

  useEffect(() => {
    document.title = `Cloudera Covid Advisor | Locations `;
  }, []);

  // console.log(locations[locationType]);
  function locationClick(e) {
    console.log("location clickedd", e.object);
    const tooltipitem = document.getElementById("tooltipitem");
    tooltipitem.style.top = e.y - 10 + "px";
    tooltipitem.style.left = e.x + 15 + "px";
    setSelectedLocation(e.object);
  }

  return (
    <div className="">
      <div className="  ">
        <DeckGL initialViewState={INITIAL_VIEW_STATE} controller={true}>
          <MapView id="map" width="100%" controller={true}>
            <StaticMap mapboxApiAccessToken={MAPBOX_ACCESS_TOKEN} />
          </MapView>

          <HeatmapLayer
            id="heatmap-plot"
            data={locationCordinates}
            opacity={0.2}
            getPosition={(d) => d.coords}
          />

          <ScatterplotLayer
            id="locations-scatter-plot"
            data={locationCordinates}
            pickable={true}
            opacity={0.8}
            radiusMinPixels={8}
            getPosition={(d) => d.coords}
            getRadius={(d) => 1900}
            getFillColor={(d) => textToRGB(d.risk?.color)}
            getLineColor={(d) => [0, 0, 0]}
            onClick={locationClick}
            onMouseEnter={locationClick}
          />
          {/* <LineLayer id="line-layer" data={lineData} /> */}
          {/* <ArcLayer
            id="connection-line-layer"
            data={connectionData}
            // greatCircle={true}
            pickable
            getWidth={1}
            // getSourcePosition={(d) => d.sourcePosition}
            // getTargetPosition={(d) => d.targetPosition}
            getSourceColor={(d) => textToRGB(d.sourceRisk.color)}
            getTargetColor={(d) => textToRGB(d.targetRisk.color)}
          /> */}
        </DeckGL>
      </div>

      <div
        id="tooltipitem"
        className="absolute -left-10 p-3 shadow rounded-sm bg-white"
      >
        {" "}
        <div
          className={"h-2 mb-1 bg-" + selectedLocation.risk?.color + "-500"}
        ></div>
        {selectedLocation.location}
      </div>

      <div className="absolute ml-2 ">
        <OfficeSelector
          locations={locations[locationType]}
          trends={trends}
          setLocationType={setLocationType}
          locationType={locationType}
        />
        <OfficeRisk locations={locations[locationType]} trends={trends} />
        <LocationChart
          locations={locations[locationType]}
          trends={trends}
          selectedLocation={selectedLocation}
        />
      </div>
    </div>
  );
};

// const locationsLayer = new ScatterplotLayer({
//   id: "locations-scatterplot-layer",
//   locationsData,
//   pickable: true,
//   opacity: 0.8,
//   stroked: true,
//   filled: true,
//   radiusScale: 6,
//   radiusMinPixels: 1,
//   radiusMaxPixels: 100,
//   lineWidthMinPixels: 1,
//   getPosition: (d) => d,
//   getRadius: (d) => 100,
//   getFillColor: (d) => [255, 140, 0],
//   getLineColor: (d) => [0, 0, 0],
// });

export default OfficeLocations;
