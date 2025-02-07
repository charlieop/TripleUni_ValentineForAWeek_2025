import "@/composables/cos";
const BUCKET = "boatonland-1307992092";
const REGION = "ap-beijing";
const URL = `https://upload.uuunnniii.com/index.php?bucket=${BUCKET}&region=${REGION}`;
const HOST = "https://i.boatonland.com/";

export const upload = (file, path) => {
  const cos = new COS({
    ForcePathStyle: true,
    getAuthorization(options, callback) {
      let xhr = new XMLHttpRequest();
      xhr.open("GET", URL, true);
      xhr.onload = function (e) {
        try {
          var data = JSON.parse(e.target.responseText);
          var credentials = data.credentials;
        } catch (e) {
          console.log(e);
        }
        if (!data || !credentials) {
          return console.error(
            "credentials invalid:\n" + JSON.stringify(data, null, 2)
          );
        }
        callback({
          TmpSecretId: credentials.tmpSecretId,
          TmpSecretKey: credentials.tmpSecretKey,
          SecurityToken: credentials.sessionToken,
          StartTime: data.startTime,
          ExpiredTime: data.expiredTime,
        });
      };
      xhr.send();
    },
  });

  return new Promise((resolve, reject) => {
    cos.putObject(
      {
        Bucket: BUCKET,
        Region: REGION,
        Key: path + randomString() + getExt(file.name),
        StorageClass: "STANDARD",
        Body: file,
      },
      function (err, data) {
        if (data.Location) {
          let location =
            HOST +
            path +
            data.Location.substr(data.Location.lastIndexOf("/") + 1);
          resolve(location);
        } else {
          reject();
        }
      }
    );
    // cos.getBucket(
    //   {
    //     Bucket: BUCKET,
    //     Region: REGION,
    //   },
    //   function (err, data) {
    //     if (data.Contents.length > 0) {
    //       resolve(err || data.Contents);
    //     } else {
    //       reject();
    //     }
    //   }
    // );
  });
};
const randomString = (e) => {
  e = e || 32;
  let t = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678",
    a = t.length,
    n = "";
  for (let i = 0; i < e; i++) n += t.charAt(Math.floor(Math.random() * a));
  return n;
};
export const getExt = (filename) => {
  let idx = filename.lastIndexOf(".");
  return idx < 1 ? "" : "." + filename.substr(idx + 1);
};
