changeActive = (name) => {
  if (name == "mysql") {
    $("#mysqlHead").addClass("active");
    $("#mysqlLikeHead").removeClass("active");
    $("#mongoDBHead").removeClass("active");
    $("#elasticSearchHead").removeClass("active");
    $("#elasticSearchDirectHead").removeClass("active");
  } else if (name == "mysqlLike") {
    $("#mysqlHead").removeClass("active");
    $("#mysqlLikeHead").addClass("active");
    $("#mongoDBHead").removeClass("active");
    $("#elasticSearchHead").removeClass("active");
    $("#elasticSearchDirectHead").removeClass("active");
  } else if (name == "mongodb") {
    $("#mysqlHead").removeClass("active");
    $("#mysqlLikeHead").removeClass("active");
    $("#mongoDBHead").addClass("active");
    $("#elasticSearchHead").removeClass("active");
    $("#elasticSearchDirectHead").removeClass("active");
  } else if (name == "elasticsearch") {
    $("#mysqlHead").removeClass("active");
    $("#mysqlLikeHead").removeClass("active");
    $("#mongoDBHead").removeClass("active");
    $("#elasticSearchHead").addClass("active");
    $("#elasticSearchDirectHead").removeClass("active");
  } else if (name == "elasticsearchdirect") {
    $("#mysqlHead").removeClass("active");
    $("#mysqlLikeHead").removeClass("active");
    $("#mongoDBHead").removeClass("active");
    $("#elasticSearchHead").removeClass("active");
    $("#elasticSearchDirectHead").addClass("active");
  }
};

showBody = (name) => {
  if (name == "mysql") {
    $("#mysql").show();
    $("#mysqlLike").hide();
    $("#mongoDB").hide();
    $("#elasticSearch").hide();
    $("#elasticSearchDirect").hide();
  } else if (name == "mysqlLike") {
    $("#mysql").hide();
    $("#mysqlLike").show();
    $("#mongoDB").hide();
    $("#elasticSearch").hide();
    $("#elasticSearchDirect").hide();
  } else if (name == "mongodb") {
    $("#mysql").hide();
    $("#mysqlLike").hide();
    $("#mongoDB").show();
    $("#elasticSearch").hide();
    $("#elasticSearchDirect").hide();
  } else if (name == "elasticsearch") {
    $("#mysql").hide();
    $("#mysqlLike").hide();
    $("#mongoDB").hide();
    $("#elasticSearch").show();
    $("#elasticSearchDirect").hide();
  } else if (name == "elasticsearchdirect") {
    $("#mysql").hide();
    $("#mysqlLike").hide();
    $("#mongoDB").hide();
    $("#elasticSearch").hide();
    $("#elasticSearchDirect").show();
  }
};

showBody("mysql");

$("#mysqlHead").on("click", () => {
  changeActive("mysql");
  showBody("mysql");
});

$("#mysqlLikeHead").on("click", () => {
  changeActive("mysqlLike");
  showBody("mysqlLike");
});

$("#mongoDBHead").on("click", () => {
  changeActive("mongodb");
  showBody("mongodb");
});

$("#elasticSearchHead").on("click", () => {
  changeActive("elasticsearch");
  showBody("elasticsearch");
});

$("#elasticSearchDirectHead").on("click", () => {
  changeActive("elasticsearchdirect");
  showBody("elasticsearchdirect");
});

$("#querySend").on("click", () => {
  //API CALL
  let url = "api/query/";
  let query = $("#query").val();
  let formData = new FormData();
  formData.append("query", query);
  axios.post(url, formData).then(
    function (response) {
      if (response.status == 200) {
        $("#mysql").html(response["data"]["data"]["mysql"]);
        $("#mysqlLike").html(response["data"]["data"]["mysql_like"]);
        $("#mongoDB").html(response["data"]["data"]["mongodb"]);
        $("#elasticSearch").html(response["data"]["data"]["elasticsearch"]);
        $("#elasticSearchDirect").html(
          response["data"]["data"]["elasticsearch_direct"]
        );
      } else {
        alert("Please check the input string!!");
      }
    },
    (error) => {
      alert("Please check the input string!!");
    }
  );
});
