const fs = require('fs')
const path = require('path')


buid("evernode","index.html",1,'笔记');

function buid(dir,file,type,title) {
	
	if (fs.existsSync(path.join(__dirname, dir, file))) {
		fs.unlinkSync(path.join(__dirname, dir, file));
	}
	if(type==1){
		fileOut(path.join(__dirname, file), toHtml(dir,type,title));
	}else{
		fileOut(path.join(__dirname, dir, file), toHtml(dir,type,title));
	}
}

function toHtml(dir, type,title) {
	if(!title||title==''){
		title="目录";
	}
	let str = '<html>\r\n' +
		'<head>\r\n' +
		'  <title>'+title+'</title>\r\n' +
		'  <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />\r\n' +
		'</head>\r\n' +
		'<body>\r\n' +
		'<h1>'+title+'</h1>\r\n' +
		'<ul>\r\n';
	try {
		fs.readdirSync(path.join(__dirname, dir)).forEach(function(file) {
			if (fs.statSync(path.join(__dirname,dir, file)).isFile()) {
				if (type == 1) {
					str += '<li><a href="' + dir + '/' + file + '" >' + file + '</a></li> \r\n';
				} else {
					str += '<li><a href="' + file + '" >' + file + '</a></li> \r\n';
				}
			}else{
				if (type == 1) {
					
				}else{
					
					str += '<li><a href="' + file + '" >' + file + '</a></li> \r\n';
					buid( dir+'/'+file,'index.html', type)
				}
			}
		})
	} catch (e) {}
	str += '</ul>\r\n' +
		'</body>\r\n' +
		'</html>\r\n';
	return str;
}

function fileOut(path, data) {
	fs.writeFileSync(path, data)
}

function fileread(file) {
	fs.readFile(file, 'utf8', function(err, data) {
		if (err) console.log(err);
		console.log(data)
	})
}

function confirmEnding(str, target) {
	var start = str.length - target.length;
	var arr = str.substr(start, target.length);
	if (arr == target) {
		return true;
	}
	return false;
}