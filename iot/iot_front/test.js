// for ESM environment, need to import modules as:
// import bb, {line} from "billboard.js";
cats = [
    "cat1",
    "cat2",
    "cat3",
    "cat4",
    "cat5",
    "cat6",
    "cat7",
    "cat8",
    "cat9"
  ]

dat  =["data1", 30, 200, 100, 400, 150, 250, 50, 100, 250]
var chart = bb.generate({
    data: {
      columns: [
        dat
      ],
      type: "line", // for ESM specify as: line()
    },
    axis: {
      x: {
        type: "category",
        categories: cats
      }
    },
    bindto: "#categoryAxis"
  });
var x = 10
  setInterval(()=>{
    cats.push("cat"+x)
    dat.push(x)
    chart.load({
        columns:[dat],
        categories:cats
    })

  },1000)
