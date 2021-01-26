export function abbreviateString(value, maxLength) {
  if (value.length <= maxLength) {
    return value;
  } else {
    let retval = value.substring(0, maxLength) + " ..";
    return retval;
  }
}

function intlFormat(num) {
  return new Intl.NumberFormat().format(Math.round(num * 10) / 10);
}
export function makeFriendly(num) {
  if (num < 1 && num > 0) {
    return num;
  }
  if (Math.abs(num) >= 1000000) return intlFormat(num / 1000000) + "M";
  if (Math.abs(num) >= 1000) return intlFormat(num / 1000) + "k";
  return intlFormat(num);
}

export function loadJSONData(url) {
  return fetch(url)
    .then(function (response) {
      if (response.status !== 200) {
        console.log(
          "Looks like there was a problem. Status Code: " + response.status
        );
        return;
      }
      // Examine the text in the response
      //    response.text().then(function(data){
      //        console.log(data)
      //    })
      return response.json().then(function (data) {
        return data;
      });
    })
    .catch(function (err) {
      return Promise.reject(err);
    });
}

export function postJSONData(url, postData) {
  return fetch(url, {
    method: "post",
    body: JSON.stringify(postData),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then(function (response) {
      if (response.status !== 200) {
        console.log(
          "Looks like there was a problem. Status Code: " + response.status
        );
        return Promise.reject(response.status);
      }
      return response.json().then(function (data) {
        return data;
      });
    })
    .catch(function (err) {
      return Promise.reject(err);
    });
}

export function uploadFile(url, postData) {
  return fetch(url, {
    method: "post",
    body: postData,
  })
    .then(function (response) {
      if (response.status !== 200) {
        console.log(
          "Looks like there was a problem. Status Code: " + response.status
        );
        return Promise.reject(response.status);
      }
      return response.json().then(function (data) {
        return data;
      });
    })
    .catch(function (err) {
      return Promise.reject(err);
    });
}

export function getFileFromUrl(url, defaultType = "image/jpeg") {
  return fetch(url, {})
    .then(function (response) {
      if (response.status !== 200) {
        console.log(
          "Looks like there was a problem. Status Code: " + response.status
        );
        return Promise.reject(response.status);
      }
      return response.blob().then(function (data) {
        return new File(
          [data],
          "File : " + response.headers.get("content-type"),
          {
            type: response.headers.get("content-type") || defaultType,
          }
        );
      });
    })
    .catch(function (err) {
      return Promise.reject(err);
    });
}

export function getElement(id) {
  return document.getElementById(id);
}

export function ColorArray() {
  let colorArray = [
    "#1f78b4",
    "#b2df8a",
    "#33a02c",
    "#fb9a99",
    "#e31a1c",
    "#fdbf6f",
    "#ff7f00",
    "#6a3d9a",
    "#cab2d6",
    "#ffff99",
    "#8fff4f",
  ];
  return colorArray;
}

export function textToRGB(text) {
  let color = [0, 0, 0];
  switch (text) {
    case "red":
      color = [239, 68, 68];
      break;
    case "yellow":
      color = [245, 158, 11];
      break;
    case "green":
      color = [16, 185, 129];
      break;
    default:
      color = [0, 0, 0];
  }
  return color;
}

export function ColorArrayRGB() {
  let colorArray = [
    [141, 211, 199],
    [255, 255, 179],
    [190, 186, 218],
    [251, 128, 114],
    [128, 177, 211],
    [253, 180, 98],
    [179, 222, 105],
    [252, 205, 229],
    [188, 128, 189],
    [204, 235, 197],
  ];
  return colorArray;
}
