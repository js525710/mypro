$.views.settings.allowCode(true);
$.views.converters("getResponseModelName", function (val) {
    return getResponseModelName(val);
});

function close_msg(){
    $(".layui-layer.layui-layer-dialog.layui-layer-border.layui-layer-msg")[0].style.display = 'none';
}

var tempBody = $.templates('#temp_body');
var tempBodyRefModel = $.templates('#temp_body_ref_model');
var tempBodyType = $.templates('#temp_body_type');


//获取context path
var contextPath = getContextPath();
console.log(contextPath)

function getContextPath() {
    var pathName = document.location.pathname;
    var index = pathName.substr(1).indexOf("/");
    var result = pathName.substr(0, index + 1);
    var result = result + '/api';
    return result;
}

$(function () {
var tags;
$.ajax({
        url: "../api/doc/gettags",
	    // url : "https://petstore.swagger.io/v2/swagger.json",
        dataType: "json",
        type: "get",
        async: false,
        success: function (data) {
            var tagsData = eval(data);
            tags = data.data;

            $.ajax({
        url: "../swagger/?format=openapi",
	    // url : "https://petstore.swagger.io/v2/swagger.json",
        dataType: "json",
        type: "get",
        async: false,
        success: function (data) {
            //layui init
            layui.use(['layer', 'jquery', 'element'], function () {
                var $ = layui.jquery, layer = layui.layer, element = layui.element;
            });
            var jsonData = eval(data);
            jsonData['tags'] = tags;

            for(var key in jsonData['paths']){
                try{
                        delete jsonData['paths'][key].parameters;
                        for (var key1 in jsonData['paths'][key]){
                            jsonData['paths'][key][key1]['consumes']=jsonData['paths'][key][key1]['tags'][1];
                            jsonData['paths'][key][key1]['produces']=jsonData['paths'][key][key1]['tags'][2];

                            if (jsonData['paths'][key][key1]['parameters'][0]['name'] == 'data'){
                                var schema = jsonData['paths'][key][key1]['parameters'][0]['schema'];
                                var parameters = new Array();
                                for (var name in schema['properties']){
                                    var param = {};
                                    param.name = name;
                                    param.type = schema['properties'][name]['type'];
                                    if (param.type=='boolean'){
                                        param.type = 'file';
                                    }
                                    param.in = 'body';
                                    param.default = 'dfasdf';
                                    param.description = schema['properties'][name]['description'];
                                    if (schema['required'].indexOf(name) >=0){
                                        param.required = true;
                                    }else{
                                        param.required = false;
                                    }
                                    parameters.push(param);
                                }
                                //jsonData['paths'][key][key1]['parameters'][0] = parameters;
                            }
                            if (jsonData['paths'][key][key1]['parameters'].length > 1){
                                parameters.push(jsonData['paths'][key][key1]['parameters'][1]);
                            }
                            jsonData['paths'][key][key1]['parameters'] = parameters;
                        }
                    }catch (err){
                    }
            }
            console.log(jsonData);

            $("#title").html(jsonData.info.title);
            $("body").html($("#template").render(jsonData));

            $("[name='a_path']").click(function () {
                var path = $(this).attr("path");
                var method = $(this).attr("method");
                var operationId = $(this).attr("operationId");
                $.each(jsonData.paths[path], function (i, d) {
                    if (d.operationId == operationId) {
                        d.path = path;
                        d.method = method;
                        $("#path-body").html(tempBody.render(d));

                        try{
                             //系统错误码
                            if(d.responses["210"]["schema"].hasOwnProperty("type")){
                                var model = {"type":d.responses["210"]["schema"]["type"]};
                                $("#path-body-response-model").append(tempBodyType.render(model));
                                // continue
                            }
                            var modelName = getRefName(d.responses["210"]["schema"]["$ref"]);
                            if(d.parameters){
                                $.each(d.parameters, function (i, p) {
                                    if (p["schema"]) {
                                        var parameterModelName = getRefName(p["schema"]["$ref"]);
                                        renderRefModel("path-body-request-model", jsonData, parameterModelName);
                                    }
                                });
                            }
                             renderRefModel("path-body-response-model", jsonData, modelName);
                        }catch(err){}

                        //如果没有返回值，直接跳过
                        if(!d.responses["200"].hasOwnProperty("schema")){
                            // continue
                            return true;
                        }

                        //基本类型
                        if(d.responses["200"]["schema"].hasOwnProperty("type")){
                            var model = {"type":d.responses["200"]["schema"]["type"]};
                            $("#path-body-response-model").append(tempBodyType.render(model));
                            // continue
                            return true;
                        }

                        //引用类型
                        var modelName = getRefName(d.responses["200"]["schema"]["$ref"]);
                        if(d.parameters){
                            $.each(d.parameters, function (i, p) {
                                if (p["schema"]) {
                                    var parameterModelName = getRefName(p["schema"]["$ref"]);
                                    renderRefModel("path-body-request-model", jsonData, parameterModelName);
                                }
                            });
                        }
                        renderRefModel("path-body-response-model", jsonData, modelName);

                    }
                });
            });

            //提交测试按钮
            $("[name='btn_submit']").click(function () {
                var operationId = $(this).attr("operationId");
                var parameterJson = {};
                $("input[operationId='" + operationId + "']").each(function (index, domEle) {
                    var k = $(domEle).attr("name");
                    var v = $(domEle).val();
                    parameterJson.push({k: v});
                });
            });
        }
    });

        }
    });

});


/**
 * 渲染ref类型参数
 * @param domId 需要添加的domId
 * @param jsonData
 * @param modelName
 */
function renderRefModel(domId, jsonData, modelName) {
    if (modelName) {
        var model = jsonData.definitions[modelName];
        model.name = modelName;
        model.domId = domId;
        //修改有嵌套对象的type
        $.each(model.properties, function (i, v) {
            if (v.items) {
                $.each(v.items, function (j, item) {
                    var typeModel = item.startsWith("#") ? getRefName(item) : item;
                    model.properties[i].type = "Array[" + typeModel + "]";
                });
            }

            //自定义对象类型（非Array）
            if (!v.type) {
                model.properties[i].type = getRefName(v["$ref"]);
            }
        });
        //如果该对象没有被渲染到页面，则渲染
        if ($("#ref-" + domId + "-" + modelName).length == 0) {
            console.log(tempBodyRefModel.render(model));
            $("#" + domId).append(tempBodyRefModel.render(model));
            console.log(tempBodyRefModel.render(model));
        }

        //递归渲染多层对象嵌套
        $.each(model.properties, function (i, v) {
            //Array
            if (v.items) {
                $.each(v.items, function (j, item) {

                    if (item.startsWith("#")) {
                        renderRefModel(domId, jsonData, getRefName(item));
                    }
                });
            }

            //单个对象引用
            if(v.hasOwnProperty("$ref")){
                renderRefModel(domId, jsonData, getRefName(v["$ref"]));
            }

        });
    }
}

//获得模型名字
function getRefName(val) {
    if (!val) {
        return null;
    }
    return val.substring(val.lastIndexOf("/") + 1, val.length);
}

//测试按钮，获取数据
function getData(operationId) {
    var path = contextPath + $("[m_operationId='" + operationId + "']").attr("path");
    //path 参数
    $("[p_operationId='" + operationId + "'][in='path']").each(function (index, domEle) {
        var k = $(domEle).attr("name");
        var v = $(domEle).val();
        if (v) {
            path = path.replace("{" + k + "}", v);
        }
    });

    //header参数
    var headerJson = {};
    $("[p_operationId='" + operationId + "'][in='header']").each(function (index, domEle) {
        var k = $(domEle).attr("name");
        var v = $(domEle).val();
        if (v) {
            headerJson[k] = v;
        }
    });

    //请求方式
    var parameterType = $("#content_type_" + operationId).val();

    //query 参数
    var parameterJson = {};
    if ("form" == parameterType) {
        $("[p_operationId='" + operationId + "'][in='query']").each(function (index, domEle) {
            var k = $(domEle).attr("name");
            var v = $(domEle).val();
            if (v) {
                parameterJson[k] = v;
            }
        });
        $("[p_operationId='" + operationId + "'][in='body']").each(function (index, domEle) {
            var k = $(domEle).attr("name");
            var v = $(domEle).val();
            if (v) {
                parameterJson[k] = v;
            }
        });
    } else if ("json" == parameterType) {
        var str = $("#text_tp_" + operationId).val();
        try {
            parameterJson = str;
        } catch (error) {
            layer.msg("" + error, {icon: 5});
            return false;
        }
    }

    //发送请求
    send(path, operationId, headerJson, parameterJson);
}


/**
 * 请求类型
 */
function changeParameterType(el) {
    var operationId = $(el).attr("operationId");
    var type = $(el).attr("type");
    $("#content_type_" + operationId).val(type);
    $(el).addClass("layui-btn-normal").removeClass("layui-btn-primary");
    if ("form" == type) {
        $("#text_tp_" + operationId).hide();
        $("#table_tp_" + operationId).show();
        $("#pt_json_" + operationId).addClass("layui-btn-primary").removeClass("layui-btn-normal");
    } else if ("json" == type) {
        var eles = $("#table_tp_" + operationId +" tr");
        var jsons = {};
        for (var i=1;i<eles.length;i++){
            ele = eles[i];
            key = ele.children[0].innerText;
            if (ele.children[1].children[0].value == ""){
                t = ele.children[4].innerText;
                if (t == 'integer'){
                    jsons[key] = 0;
                }
                if (t == 'boolean'){
                    jsons[key] = false;
                }
                if (t == 'string'){
                    jsons[key] = "";
                }
            }else{
                jsons[key] = ele.children[1].children[0].value;
            }
        }
        $("#text_tp_" + operationId)[0].value = JSON.stringify(jsons,null,'\t');
        $("#text_tp_" + operationId).show();
        $("#table_tp_" + operationId).hide();
        $("#pt_form_" + operationId).addClass("layui-btn-primary").removeClass("layui-btn-normal");
    }
}

/**
 * 发送请求
 * @param url 地址
 * @param operationId   operationId
 * @param header    header参数
 * @param data  data数据
 */
function send(url, operationId, header, data) {

    var type = $("[m_operationId='" + operationId + "']").attr("method");

    //是否有formData类型数据
    var hasFormData = $("[p_operationId='" + operationId + "'][in='query']").length >= 1;

    //是否有body类型数据
    var hasBody = $("[p_operationId='" + operationId + "'][in='body']").length >= 1;

    var options = {withQuotes: true};

    //发送请求
    if (hasFormData) {
        var formData = $("#form_" + operationId).serialize();
        $.ajax({
            type: type,
            url: url,
            headers: header,
            data: formData,
            dataType: 'json',
            cache: false,
            processData: false,
            contentType: false,
            success: function (data) {
                $("#json-response").jsonViewer(data, options);
            },
            error:function(e){
                $("#json-response").html("");
                layer.msg("" + JSON.stringify(e), {icon: 5});
            }
        });
        return;
    }

    //querystring ,将参数加在url后面
//    url = appendParameterToUrl(url,data);

    //requestBody 请求
    var bodyData ;
    if (hasBody) {
//        var dom = $("[p_operationId='" + operationId + "'][in='body']")[0];
        bodyData = data;
        }
    try{
        file = $("[p_operationId='" + operationId + "'][in='body']")[0].files[0];
        formData = new FormData();
        formData.append('file',file);
        bodyData = formData;
        $.ajax({
            url : url,
            type : 'POST',
            data : formData,
            // 告诉jQuery不要去处理发送的数据
            processData : false,
            // 告诉jQuery不要去设置Content-Type请求头
            contentType : false,
            dataType : "json",
            success: function (data) {
                    $("#json-response").jsonViewer(data, options);
                },
            error:function(e){
                $("#json-response").html("");
                layer.msg("" + JSON.stringify(e), {icon: 5});
            }
        });
        return;
    }catch(err){};

    var contentType = $("#consumes_" + operationId).text();

    $.ajax({
        type: type,
        url: url,
        headers: header,
        data: data,
        dataType: 'json',
        contentType: contentType,
        success: function (data) {
            $("#json-response").jsonViewer(data, options);
        },
        error:function(e){
            $("#json-response").html("");
            layer.msg("" + JSON.stringify(e), {icon: 5});
        }
    });
}

/**
 * 给url拼装参数
 * @param url
 * @param parameter
 */
function appendParameterToUrl(url, parameter) {
    if($.isEmptyObject(parameter)){
        return url;
    }
    $.each(parameter, function (k, v) {
        if (url.indexOf("?") == -1) {
            url += "?";
        }
        url += k;
        url += "=";
        url += v;
        url += "&";
    });
    return url.substring(0, url.length - 1);
}
