var wms_layers = [];


        var lyr_OpenStreetMap_0 = new ol.layer.Tile({
            'title': 'OpenStreetMap',
            //'type': 'base',
            'opacity': 1.000000,
            
            
            source: new ol.source.XYZ({
    attributions: ' ',
                url: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
            })
        });
var format_rg1_hexgrid_base_1 = new ol.format.GeoJSON();
var features_rg1_hexgrid_base_1 = format_rg1_hexgrid_base_1.readFeatures(json_rg1_hexgrid_base_1, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_rg1_hexgrid_base_1 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_rg1_hexgrid_base_1.addFeatures(features_rg1_hexgrid_base_1);
var lyr_rg1_hexgrid_base_1 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_rg1_hexgrid_base_1, 
                style: style_rg1_hexgrid_base_1,
                popuplayertitle: "rg1_hexgrid_base",
                interactive: true,
                    title: '<img src="styles/legend/rg1_hexgrid_base_1.png" /> rg1_hexgrid_base'
                });
var format_rg1_CS_MEAN_2 = new ol.format.GeoJSON();
var features_rg1_CS_MEAN_2 = format_rg1_CS_MEAN_2.readFeatures(json_rg1_CS_MEAN_2, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_rg1_CS_MEAN_2 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_rg1_CS_MEAN_2.addFeatures(features_rg1_CS_MEAN_2);
var lyr_rg1_CS_MEAN_2 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_rg1_CS_MEAN_2, 
                style: style_rg1_CS_MEAN_2,
                popuplayertitle: "rg1_CS_MEAN",
                interactive: true,
                    title: '<img src="styles/legend/rg1_CS_MEAN_2.png" /> rg1_CS_MEAN'
                });
var format_rg1_CS_SUM_3 = new ol.format.GeoJSON();
var features_rg1_CS_SUM_3 = format_rg1_CS_SUM_3.readFeatures(json_rg1_CS_SUM_3, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_rg1_CS_SUM_3 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_rg1_CS_SUM_3.addFeatures(features_rg1_CS_SUM_3);
var lyr_rg1_CS_SUM_3 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_rg1_CS_SUM_3, 
                style: style_rg1_CS_SUM_3,
                popuplayertitle: "rg1_CS_SUM",
                interactive: true,
                    title: '<img src="styles/legend/rg1_CS_SUM_3.png" /> rg1_CS_SUM'
                });
var format_rg1_existing_rhus_4 = new ol.format.GeoJSON();
var features_rg1_existing_rhus_4 = format_rg1_existing_rhus_4.readFeatures(json_rg1_existing_rhus_4, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_rg1_existing_rhus_4 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_rg1_existing_rhus_4.addFeatures(features_rg1_existing_rhus_4);
var lyr_rg1_existing_rhus_4 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_rg1_existing_rhus_4, 
                style: style_rg1_existing_rhus_4,
                popuplayertitle: "rg1_existing_rhus",
                interactive: true,
                    title: '<img src="styles/legend/rg1_existing_rhus_4.png" /> rg1_existing_rhus'
                });
var format_rg1_OS_MEAN_5 = new ol.format.GeoJSON();
var features_rg1_OS_MEAN_5 = format_rg1_OS_MEAN_5.readFeatures(json_rg1_OS_MEAN_5, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_rg1_OS_MEAN_5 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_rg1_OS_MEAN_5.addFeatures(features_rg1_OS_MEAN_5);
var lyr_rg1_OS_MEAN_5 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_rg1_OS_MEAN_5, 
                style: style_rg1_OS_MEAN_5,
                popuplayertitle: "rg1_OS_MEAN",
                interactive: true,
                    title: '<img src="styles/legend/rg1_OS_MEAN_5.png" /> rg1_OS_MEAN'
                });
var format_rg1_OS_SUM_6 = new ol.format.GeoJSON();
var features_rg1_OS_SUM_6 = format_rg1_OS_SUM_6.readFeatures(json_rg1_OS_SUM_6, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_rg1_OS_SUM_6 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_rg1_OS_SUM_6.addFeatures(features_rg1_OS_SUM_6);
var lyr_rg1_OS_SUM_6 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_rg1_OS_SUM_6, 
                style: style_rg1_OS_SUM_6,
                popuplayertitle: "rg1_OS_SUM",
                interactive: true,
                    title: '<img src="styles/legend/rg1_OS_SUM_6.png" /> rg1_OS_SUM'
                });
var format_rg1_prioritized_SUM_7 = new ol.format.GeoJSON();
var features_rg1_prioritized_SUM_7 = format_rg1_prioritized_SUM_7.readFeatures(json_rg1_prioritized_SUM_7, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_rg1_prioritized_SUM_7 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_rg1_prioritized_SUM_7.addFeatures(features_rg1_prioritized_SUM_7);
var lyr_rg1_prioritized_SUM_7 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_rg1_prioritized_SUM_7, 
                style: style_rg1_prioritized_SUM_7,
                popuplayertitle: "rg1_prioritized_SUM",
                interactive: true,
                    title: '<img src="styles/legend/rg1_prioritized_SUM_7.png" /> rg1_prioritized_SUM'
                });
var group_rg1 = new ol.layer.Group({
                                layers: [lyr_rg1_hexgrid_base_1,lyr_rg1_CS_MEAN_2,lyr_rg1_CS_SUM_3,lyr_rg1_existing_rhus_4,lyr_rg1_OS_MEAN_5,lyr_rg1_OS_SUM_6,lyr_rg1_prioritized_SUM_7,],
                                fold: "open",
                                title: "rg1"});

lyr_OpenStreetMap_0.setVisible(true);lyr_rg1_hexgrid_base_1.setVisible(true);lyr_rg1_CS_MEAN_2.setVisible(true);lyr_rg1_CS_SUM_3.setVisible(true);lyr_rg1_existing_rhus_4.setVisible(true);lyr_rg1_OS_MEAN_5.setVisible(true);lyr_rg1_OS_SUM_6.setVisible(true);lyr_rg1_prioritized_SUM_7.setVisible(true);
var layersList = [lyr_OpenStreetMap_0,group_rg1];
lyr_rg1_hexgrid_base_1.set('fieldAliases', {'fid': 'fid', 'bg_name': 'bg_name', 'cm_name': 'cm_name', 'pr_name': 'pr_name', 'Neighbors3': 'Neighbors3', 'Neighbors': 'Neighbors', });
lyr_rg1_CS_MEAN_2.set('fieldAliases', {'fid': 'fid', 'bg_name': 'bg_name', 'cm_name': 'cm_name', 'pr_name': 'pr_name', 'Neighbors3': 'Neighbors3', 'Neighbors': 'Neighbors', });
lyr_rg1_CS_SUM_3.set('fieldAliases', {'fid': 'fid', 'bg_name': 'bg_name', 'cm_name': 'cm_name', 'pr_name': 'pr_name', 'Neighbors3': 'Neighbors3', 'Neighbors': 'Neighbors', });
lyr_rg1_existing_rhus_4.set('fieldAliases', {'fid': 'fid', 'bg_name': 'bg_name', 'cm_name': 'cm_name', 'pr_name': 'pr_name', 'Neighbors3': 'Neighbors3', 'Neighbors': 'Neighbors', });
lyr_rg1_OS_MEAN_5.set('fieldAliases', {'fid': 'fid', 'bg_name': 'bg_name', 'cm_name': 'cm_name', 'pr_name': 'pr_name', 'Neighbors3': 'Neighbors3', 'Neighbors': 'Neighbors', });
lyr_rg1_OS_SUM_6.set('fieldAliases', {'fid': 'fid', 'bg_name': 'bg_name', 'cm_name': 'cm_name', 'pr_name': 'pr_name', 'Neighbors3': 'Neighbors3', 'Neighbors': 'Neighbors', });
lyr_rg1_prioritized_SUM_7.set('fieldAliases', {'fid': 'fid', 'bg_name': 'bg_name', 'cm_name': 'cm_name', 'pr_name': 'pr_name', 'Neighbors3': 'Neighbors3', 'Neighbors': 'Neighbors', });
lyr_rg1_hexgrid_base_1.set('fieldImages', {'fid': 'TextEdit', 'bg_name': 'TextEdit', 'cm_name': 'TextEdit', 'pr_name': 'TextEdit', 'Neighbors3': 'TextEdit', 'Neighbors': 'TextEdit', });
lyr_rg1_CS_MEAN_2.set('fieldImages', {'fid': 'TextEdit', 'bg_name': 'TextEdit', 'cm_name': 'TextEdit', 'pr_name': 'TextEdit', 'Neighbors3': 'TextEdit', 'Neighbors': 'TextEdit', });
lyr_rg1_CS_SUM_3.set('fieldImages', {'fid': 'TextEdit', 'bg_name': 'TextEdit', 'cm_name': 'TextEdit', 'pr_name': 'TextEdit', 'Neighbors3': 'TextEdit', 'Neighbors': 'TextEdit', });
lyr_rg1_existing_rhus_4.set('fieldImages', {'fid': 'TextEdit', 'bg_name': 'TextEdit', 'cm_name': 'TextEdit', 'pr_name': 'TextEdit', 'Neighbors3': 'TextEdit', 'Neighbors': 'TextEdit', });
lyr_rg1_OS_MEAN_5.set('fieldImages', {'fid': 'TextEdit', 'bg_name': 'TextEdit', 'cm_name': 'TextEdit', 'pr_name': 'TextEdit', 'Neighbors3': 'TextEdit', 'Neighbors': 'TextEdit', });
lyr_rg1_OS_SUM_6.set('fieldImages', {'fid': 'TextEdit', 'bg_name': 'TextEdit', 'cm_name': 'TextEdit', 'pr_name': 'TextEdit', 'Neighbors3': 'TextEdit', 'Neighbors': 'TextEdit', });
lyr_rg1_prioritized_SUM_7.set('fieldImages', {'fid': 'TextEdit', 'bg_name': 'TextEdit', 'cm_name': 'TextEdit', 'pr_name': 'TextEdit', 'Neighbors3': 'TextEdit', 'Neighbors': 'TextEdit', });
lyr_rg1_hexgrid_base_1.set('fieldLabels', {'fid': 'header label - visible with data', 'bg_name': 'inline label - visible with data', 'cm_name': 'inline label - visible with data', 'pr_name': 'inline label - visible with data', 'Neighbors3': 'hidden field', 'Neighbors': 'hidden field', });
lyr_rg1_CS_MEAN_2.set('fieldLabels', {'fid': 'header label - visible with data', 'bg_name': 'inline label - visible with data', 'cm_name': 'inline label - visible with data', 'pr_name': 'inline label - visible with data', 'Neighbors3': 'hidden field', 'Neighbors': 'hidden field', });
lyr_rg1_CS_SUM_3.set('fieldLabels', {'fid': 'header label - visible with data', 'bg_name': 'header label - visible with data', 'cm_name': 'inline label - visible with data', 'pr_name': 'inline label - visible with data', 'Neighbors3': 'hidden field', 'Neighbors': 'hidden field', });
lyr_rg1_existing_rhus_4.set('fieldLabels', {'fid': 'header label - visible with data', 'bg_name': 'inline label - visible with data', 'cm_name': 'inline label - visible with data', 'pr_name': 'inline label - visible with data', 'Neighbors3': 'hidden field', 'Neighbors': 'hidden field', });
lyr_rg1_OS_MEAN_5.set('fieldLabels', {'fid': 'header label - visible with data', 'bg_name': 'inline label - visible with data', 'cm_name': 'inline label - visible with data', 'pr_name': 'inline label - visible with data', 'Neighbors3': 'hidden field', 'Neighbors': 'hidden field', });
lyr_rg1_OS_SUM_6.set('fieldLabels', {'fid': 'header label - visible with data', 'bg_name': 'inline label - visible with data', 'cm_name': 'inline label - visible with data', 'pr_name': 'inline label - visible with data', 'Neighbors3': 'hidden field', 'Neighbors': 'hidden field', });
lyr_rg1_prioritized_SUM_7.set('fieldLabels', {'fid': 'header label - visible with data', 'bg_name': 'inline label - visible with data', 'cm_name': 'inline label - visible with data', 'pr_name': 'inline label - visible with data', 'Neighbors3': 'hidden field', 'Neighbors': 'hidden field', });
lyr_rg1_prioritized_SUM_7.on('precompose', function(evt) {
    evt.context.globalCompositeOperation = 'normal';
});