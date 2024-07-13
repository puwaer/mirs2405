#!/usr/bin/perl

# MIRSXXXX work record CGI.
# Written by Hajime Wakabayashi.
# Since 22 Mar. 2004
# 
# 
# 
# 2015/4/26 
#	編集画面から表示画面を表示させる際に、ユーザ名が引き継がれエラーとなるバグを修正 
# 
# 2018/4/19 改訂 by S. Ushimaru
# 

use CGI;
use CGI::Cookie;
#use CGI::Carp qw(fatalsToBrowser);
use Jcode;
#use lib './';
use lib '/www/mirsdoc2/cgi-bin/record/';

require "/www/mirsdoc2/cgi-bin/record/ini.cgi";
require "/www/mirsdoc2/cgi-bin/record/common.cgi";

#state $user_name = $name;

# -------------------------------------------------------------------------- #

#	main - Main routine.

$q = new CGI;
my $mode = $q->param('mode');

if($mode eq "new") {
	&NewUser;
} elsif($mode eq "view") {
	$name = $q->param('vName');
	&Viewer($name);
} elsif($mode eq "view2") {
	$name = $q->param('user_name');
	&Viewer($name);
} elsif($mode eq "edit") {
	if ( &IsReqPass ) {
		&PassField;
	} else {
		&EditField;
	}
} elsif($mode eq "misc") {
	if ( $q->param('cErase') ) {
		&EraseCookie;
	}
} else {
	&Info;
}

exit;

# -------------------------------------------------------------------------- #

#	NewUser - Create new user.

sub NewUser {
	if ( $q->param('nSubmit') ) {
		&printheader("Work Record - New User Registration.");
		&printtop;
		&RNewUser;
		&printfooter;
	} else {
		&printheader("Work Record - New User");
		&printtop;
		&MNewUser;
		&printfooter;
	}
	return;
}

# -------------------------------------------------------------------------- #

#	Info - Display system information.

sub Info {
	&printheader("Work Record - System Information");
	&printtop;
	&MInfo;
	&printfooter;
	
	return;
}

# -------------------------------------------------------------------------- #

#	PassField - Display password entering field.

sub PassField {
	if ( $q->param('pSubmit') ) {
		&RPassword;
	} else {
		&printheader("Work Record - Password");
		&printtop;
		&MPassField;
		&printfooter;
	}
	return;
}

# -------------------------------------------------------------------------- #

#	EditField - Display data input/edit field.

sub EditField {
	if( $q->param('esSubmit') ) {
		&ChangeSettings;
	} elsif( $q->param('ewChange') ) {
		&ChangeLog;
	} elsif( $q->param('ewDelete') ) {
		&DeleteLog;
	} elsif( $q->param('ewAdd') ) {
		&AddLog;
	} elsif( $q->param('ewInsert') ) {
		&InsertLog;
	} else {
		&printheader("Work Record - Edit");
		&printtop;
		&MEditField;
		&printfooter;
	}
	
	return;
}

# -------------------------------------------------------------------------- #
# There are private routines below.
# -------------------------------------------------------------------------- #

# -------------------------------------------------------------------------- #

#	MNewUser - User registering form.

sub MNewUser {
	print <<EOF;
	<!-- User registering form -->
	<table border="0" width="100%" cellspacing="0" cellpadding="0">
		<tr><td width=100%>
		<div class=title>新しいユーザー</div>
		<div class=comment>
			<form method=POST>
				ユーザー名：<br>
				<input type=text name=nName>
				<p>
				氏名：<br>
				<input type=text name=nNameR>
<!--
				<p>
				学籍番号：<br>
				<input type=text name=nNumber>
-->
				<p>
				チーム：<br>
				<input type=text name=nTeam>
				<p>
				開発担当：<br>
				<select name=nPosition>
					<option value="O">未定
					<option value="M">メカニクス
					<option value="E">エレクトロニクス
					<option value="S">ソフトウェア
				</select>
				<p>
				役割：<br>
				<select name=nRole>
					<option value="N">
					<option value="P">プロジェクマネージャ
					<option value="L">チームリーダ
					<option value="D">ドキュメントマネージャ
					<option value="AD">広報
				</select>
				<p>
				ドキュメント番号：<br>
				<input type=text name=nDocument size="22" maxlength="18">
				<p>
				パスワード：<br>
				<input type=password name=nPass>
				<p>
				<input type=hidden name=mode value="new">
				<input type=submit name=nSubmit value="+ 登録 +">
				<p>
			</form>
	</table>
	<p>
EOF

	return;
}

# -------------------------------------------------------------------------- #

#	RNewUser - Regist new user.

sub RNewUser {
	#my($nname,$nnumber,$nteam,$ndocument,$npass,$nnamer);
	my($nname,$nteam,$ndocument,$npass,$nnamer);
	my $errormes = undef;
	$nname		= $q->param('nName');
	$nnamer		= jcode( $q->param('nNameR') )->euc;
	#$nnumber	= uc $q->param('nNumber'); 
	$nteam		= uc $q->param('nTeam');
	$npos		= uc $q->param('nPosition');
	$nrole		= uc $q->param('nRole');
	$ndocument	= uc $q->param('nDocument');
	$npass		= $q->param('nPass');
	
	if ($nname !~ /^\w{4,12}$/) {
		$errormes = "名前が不正です。";
	} elsif( &IsUserExists($nname) ) {
		$errormes = "ユーザー $nname がすでに存在します。";
#	} elsif ($nnumber !~ /^[A-Z]\d{3}$/) {
#		$errormes = "学籍番号が不正です。";
#	} elsif ($nteam !~ /^MIRS\d{4}$/) {
#		$errormes = "チームが不正です。";
	#} elsif ($npos !~ /^[MESO]$/) {
	} elsif ($npos !~ /^(M|E|S|O)/) {
		$errormes = "開発担当が不正です。";
	#} elsif ($nrole !~ /^[NPLDCSAD]$/) {
	} elsif ($nrole !~ /^(P|L|D|CS|AD|N)/) {
		$errormes = "役割が不正です。";
#	} elsif ($ndocument !~ /^MIRS\d{4}-[A-Z]+-\d+$/) {
#		$errormes = "ドキュメント番号が不正です。";
	} elsif ($npass !~ /^.{5,12}$/) {
		$errormes = "パスワードが不正です。";
	}
	
	if ($errormes) {
		&error("新規登録 - $errormes");
	} else {
		my $cpass = crypt($npass,crypt($npass,reverse($npass)));
		#my $new = "$nname<>$nnumber<>$nnamer<>$nteam<>$npos<>$nrole<>$ndocument<>$cpass<>\n";
		my $new = "$nname<>$nnamer<>$nteam<>$npos<>$nrole<>$ndocument<>$cpass<>\n";
		
		open(WRITE,">$logdir/$nname.log") or &error("例外No.1 管理者に連絡してください。");
			print WRITE $new;
		close(WRITE);
		
		print <<EOF;
	<table border="0" width="100%" cellspacing="0" cellpadding="0">
		<tr><td width=100%>
		<div class=title>新しいユーザー</div>
		<div class=comment>
			<p>
			ユーザー $nname の作成に成功しました。<br>
			<a href="$self?mode=edit">編集画面へ</a>
			<p>
		</div>
	</table>
	<p>
EOF
	}
	return;
}

# -------------------------------------------------------------------------- #

#	MPassField - Password entering form.

sub MPassField {
	print <<EOF;
	<!-- Password entering form -->
	<table border="0" width="100%" cellspacing="0" cellpadding="0">
		<tr><td width=100%>
		<div class=title>パスワード入力</div>
		<div class=comment>
			<form method=POST>
				ユーザー名：<br>
				<input type=text name=pName>
				<p>
				パスワード：<br>
				<input type=password name=pPass>
				<p>
				<input type=hidden name=mode value="edit">
				<input type=submit name=pSubmit value="+ 認証 +">
				<p>
			</form>
		</div>
	</table>
	<p>
EOF

	return;
}

# -------------------------------------------------------------------------- #

#	RPassword - Resist password.

sub RPassword {
	my $pname = $q->param('pName');
	my $ppass = $q->param('pPass');
	$ppass = crypt($ppass,crypt($ppass,reverse($ppass)));

	open(READ,"$logdir/$pname.log") or
		&error("ログファイルが開けません。管理者に連絡してください。");
		@foo = split("<>",<READ>);
	close(READ);
	my $lpass = $foo[6];
	#my $lpass = $foo[7];
	if( $ppass eq $lpass ) {
		my $c = new CGI::Cookie(
			-name    =>  "mirswr",
			-value   =>  "$pname-$ppass-",
			-expires =>  $expires,
			-domain  =>  $domain,
		);
		print "Set-Cookie: $c\n";
		&backto("$self?mode=edit");
		return 1;
	} else {
		&error2("パスワードかユーザー名が違います。");
		return 0;
	}
}

# -------------------------------------------------------------------------- #

#	MInfo - Main routine of Info.

sub MInfo {
	print <<EOF;
	<!-- System Information -->
	<table border="0" width="100%" cellspacing="0" cellpadding="0">
		<tr><td width=100%>
		<div class=title>ユーザー一覧</div>
		<div class=comment>
			<p>
			<table border="0" width="550" cellspacing="0" cellpadding="0">
			<!-- <tr bgcolor=#D0D0D0><td>名前<td>学籍番号<td>チーム<td>開発担当<td>役割<td>ドキュメント番号<td>更新日時 -->
			<tr bgcolor=#D0D0D0><td>ユーザ名<td>名前<td>チーム<td>開発担当<td>役割<td>ドキュメント番号<td>更新日時
EOF
	if( (-e $logdir) && opendir(DH, $logdir) ) {
		while(my $file = readdir DH) {
			if($file =~ ".log") {
				open(READ, "$logdir/$file");
					my $udata = <READ>;
				close(READ);
				my $mtime = &fixedtime((stat("$logdir/$file"))[9]);
				#my $mtime = &fixedtime((stat("$logdir/$file"))[10]);
				#my($uname, $unum, $unamer, $uteam, $upos, $urole, $udoc, $upass) = split("<>", $udata);
				my($uname, $unamer, $uteam, $upos, $urole, $udoc, $upass) = split("<>", $udata);
				if($upos eq 'M')    { $upos = "メカニクス"; }
				elsif($upos eq 'E') { $upos = "エレクトロニクス"; }
				elsif($upos eq 'S') { $upos = "ソフトウェア"; }
				elsif($upos eq 'O') { $upos = "未定"; }
				else {$upos = "不明"; }

				if($urole eq 'P')    { $urole = "プロジェクトマネージャ"; }
				elsif($urole eq 'L') { $urole = "チームリーダ"; }
				elsif($urole eq 'D') { $urole = "ドキュメントマネージャ"; }
				elsif($urole eq 'AD') { $urole = "広報"; }
				elsif($urole eq 'N') { $urole = ""; }
				else {$urole = "不明"; }
				
				#print "\t\t\t<tr><td><a href=\"$self?mode=view&vName=$uname\">$unamer</a><td>$unum<td>$uteam<td>$upos<td>$urole<td>$udoc<td>$mtime\n";
				#print "\t\t\t<tr><td><a href=\"$self?mode=view&vName=$uname\">$unamer</a><td>$uteam<td>$upos<td>$urole<td>$udoc<td>$mtime\n";
				print "\t\t\t<tr><td><a href=\"$self?mode=view&vName=$uname\">$uname</a><td>$unamer<td>$uteam<td>$upos<td>$urole<td>$udoc<td>$mtime\n";
			}
		}
	}
	print <<EOF;
			</table>
		</div>
		<p>
	</table>
	<p>
	<table border="0" width="100%" cellspacing="0" cellpadding="0">
		<tr><td width=100%>
		<div class=title>その他</div>
		<div class=comment>
			<p>
			クッキーを消すには次のボタンをクリックしてください。
			<form method=POST>
				<input type=hidden name=mode value=misc>
				<input type=submit name=cErase value="+ 消去 +">
			</form>
			<p>
		</div>
	</table>
	<p>
EOF
	&ShowAbout;
	return;
}
# -------------------------------------------------------------------------- #

#	Viewer - User data viewer.

sub Viewer {
	my $name = $_[0];
	if(!$name or !&IsUserExists($name) ) {
		&error2("ユーザー名が間違っています。");
	}
	my $rpass;
	if($name eq &GetUser) {
		$rpass = 0;
	} else {
		$rpass = 1;
	}
	
	&printheader("Work Record - User Data Viewer");
	&printtop;
	
	open(READ, "$logdir/$name.log");
		my @data = <READ>;
	close(READ);
	my $mtime = &fixedtime((stat("$logdir/$name.log"))[9]);
	#my($name, $num, $namer, $team, $pos, $role, $doc, $pass) = split("<>", $data[0]);
	my($name, $namer, $team, $pos, $role, $doc, $pass) = split("<>", $data[0]);
	
	if($pos eq 'M')    { $pos = "メカニクス"; }
	elsif($pos eq 'E') { $pos = "エレクトロニクス"; }
	elsif($pos eq 'S') { $pos = "ソフトウェア"; } 
	elsif($pos eq 'O') { $pos = "未定"; }
	else { $pos = "不明"; }
	
	if($role eq 'P')    { $role = "プロジェクトマネージャ"; }
	elsif($role eq 'L') { $role = "チームリーダー"; }
	elsif($role eq 'D') { $role = "ドキュメントマネージャ"; }
	elsif($role eq 'AD') { $role = "広報"; }
	elsif($role eq 'N') { $role = ""; }
	else { $role = "不明"; }
	
	print <<EOF;
	<table border="0" width="100%" cellspacing="0" cellpadding="0">
		<!-- <tr bgcolor=#D0D0D0><td>名前<td>学籍番号<td>チーム<td>開発担当<td>役割<td>ドキュメント番号<td>更新日時 -->
		<!-- <tr><td>$namer<td>$num<td>$team<td>$pos<td>$role<td>$doc<td>$mtime -->
		<tr bgcolor=#D0D0D0><td>名前<td>チーム<td>開発担当<td>役割<td>ドキュメント番号<td>更新日時
		<tr><td>$namer<td>$team<td>$pos<td>$role<td>$doc<td>$mtime
	</table>
	<p>
EOF
	if(!$data[1]) {
		print <<EOF;
	<table border="0" width="100%" cellspacing="0" cellpadding="0">
		<tr><td width=100%>
		<div class=comment>
			<p>
			作業記録データは入力されていません。
			<p>
		</div>
	</table>
	<p>
EOF
	} else {
		print <<EOF;
	<table border="0" width="100%" cellspacing="0" cellpadding="0">
		<tr bgcolor=#D0D0D0>
			<!-- <td>日付<td>作業コード<td>作業内容<td>授業内作業(H)<td>授業外作業(H)<td>備考 -->
			<td>日付<td>作業コード<td>作業内容<td>作業時間(H)<td>備考
EOF
		my $h1sum=0;
                my $h01sum=0;
                my $h02sum=0;
                my $h03sum=0;
                my $h10sum=0;
                my $h11sum=0;
                my $h12sum=0;
                my $h13sum=0;
                my $h14sum=0;
                my $h20sum=0;
                my $h21sum=0;
                my $h22sum=0;
                my $h23sum=0;
                my $h30sum=0;
                my $h31sum=0;
                my $h32sum=0;
                my $h40sum=0;
                my $h41sum=0;
                my $h42sum=0;
                my $h50sum=0;
                my $h51sum=0;
                my $h52sum=0;
                my $h60sum=0;

		#my $h2sum=0;
		for(my $i=1;$i<=$#data;$i++) {
			#my($date, $code, $work, $h1, $h2, $note) = split("<>", $data[$i]);
			my($date, $code, $work, $h1, $note) = split("<>", $data[$i]);
			$h1sum+=$h1;
                        if($code eq "01") {$h01sum+=$h1;}
                        if($code eq "02") {$h02sum+=$h1;}
                        if($code eq "03") {$h03sum+=$h1;}
                        if($code eq "10") {$h10sum+=$h1;}
                        if($code eq "11") {$h11sum+=$h1;}
                        if($code eq "12") {$h12sum+=$h1;}
                        if($code eq "13") {$h13sum+=$h1;}
                        if($code eq "14") {$h14sum+=$h1;}
                        if($code eq "20") {$h20sum+=$h1;}
                        if($code eq "21") {$h21sum+=$h1;}
                        if($code eq "22") {$h22sum+=$h1;}
                        if($code eq "23") {$h23sum+=$h1;}
                        if($code eq "30") {$h30sum+=$h1;}
                        if($code eq "31") {$h31sum+=$h1;}
                        if($code eq "32") {$h32sum+=$h1;}
                        if($code eq "40") {$h40sum+=$h1;}
                        if($code eq "41") {$h41sum+=$h1;}
                        if($code eq "42") {$h42sum+=$h1;}
                        if($code eq "50") {$h50sum+=$h1;}
                        if($code eq "51") {$h51sum+=$h1;}
                        if($code eq "52") {$h52sum+=$h1;}
                        if($code eq "60") {$h60sum+=$h1;}

			#$h2sum+=$h2;
			$work =~ s/\n/<br>/g;
			$note="<br>" if($note eq "");
			
			#print "\t\t\t<tr><td width=100>$date<td width=100>$code<td>$work<td width=100>$h1<td width=100>$h2<td width=100>$note\n";
			print "\t\t\t<tr><td width=100>$date<td width=100>$code<td>$work<td width=100>$h1<td width=100>$note\n";
		}
			#print "\t\t\t<tr><td width=100><br><td width=100><br><td>合計時間<td width=100>$h1sum<td width=100>$h2sum<td width=100><br>\n";
			print "\t\t\t<tr><td width=100><br><td width=100><br><td>合計時間<td width=100>$h1sum<td width=100><br>\n";
		print <<EOF;
		</tr>
	</table>
	<p>

	<table border="0" width="100%" cellspacing="0" cellpadding="0">
		<tr bgcolor=#D0D0D0><td>作業<td>時間<td>作業<td>時間<td>作業<td>時間<td>作業<td>時間
		<tr><td>01:ミーティング<td>$h01sum<td>02:ドキュメントレビュー<td>$h02sum<td>03:ドキュメント整備<td>$h03sum<td>10:MIRS解体<td>$h10sum
		<tr><td>11:標準部品製造・試験<td>$h11sum<td>12:標準機機能試験<td>$h12sum<td>13:デモ競技プログラム開発<td>$h13sum<td>14:標準機統合試験<td>$h14sum
		<tr><td>20:技術調査・製品企画<td>$h20sum<td>21:企画、システム提案、開発計画立案<td>$h21sum<td>22:システム基本設計<td>$h22sum<td>23:システム統合試験<td>$h23sum
		<tr><td>30:メカ詳細設<td>$h30sum<td>31:エレキ詳細設計<td>$h31sum<td>32:ソフト詳細設計<td>$h32sum<td><br><td><br>
		<tr><td>40:メカ製造・試験<td>$h40sum<td>41-エレキ製造・試験<td>$h41sum<td>42-ソフト実装・試験<td>$h42sum<td><br><td><br>
		<tr><td>50:発表会システム開発<td>$h50sum<td>51:社会実装実験<td>$h51sum<td>52:発表会準備<td>$h52sum<td>60:その他<td>$h60sum
	</table>
EOF
	}
	if ( $rpass ) {
		print <<EOF;
	<form method=POST>
		<table border="0" width="100%" cellspacing="0" cellpadding="0">
			<tr align><td width=100%>
				ユーザー名：<input type=text name="pName" value="$name">
				パスワード：<input type=password name="pPass">
				<input type=submit name="pSubmit" value="認証">
				<input type=hidden name="mode" value="edit">
		</table>
	</form>
EOF
	} else {
		print <<EOF;
	<form method=POST>
		<table border="0" width="100%" cellspacing="0" cellpadding="0">
			<tr><td width=100%>
				<input type=submit name="pSubmit" value="編集画面に進む">
				<input type=hidden name="mode" value="edit">
		</table>
	</form>
EOF
	}
	&printfooter;
	return;
}

# -------------------------------------------------------------------------- #

#	MEditField - Edit field.

sub MEditField {
	%cookies = fetch CGI::Cookie;
	my($cdata, $cname, $cpass, @data);
	
	if ( $cookies{'mirswr'} ) {
		$cdata = $cookies{'mirswr'}->value;
		($cname, $cpass) = split("-", $cdata);
	}

	open(READ, "$logdir/$cname.log");
		@data = <READ>;
	close(READ);
	my $mtime = &fixedtime((stat("$logdir/$cname.log"))[9]);
	#my $mtime = &fixedtime((stat("$logdir/$cname.log"))[10]);
	#my($name, $num, $namer, $team, $pos, $role, $doc, $pass) = split("<>", $data[0]);
	my($name, $namer, $team, $pos, $role, $doc, $pass) = split("<>", $data[0]);
	
	if($pos eq 'M')    { $mpos = "selected"; }
	elsif($pos eq 'E') { $epos = "selected"; }
	elsif($pos eq 'S') { $spos = "selected"; }
	elsif($pos eq 'O') { $opos = "selected"; }
	
	if($role eq 'P')    { $prole = "selected"; }
	elsif($role eq 'L') { $lrole = "selected"; }
	elsif($role eq 'D') { $drole = "selected"; }
	elsif($role eq 'CS') { $csrole = "selected"; }
	elsif($role eq 'AD') { $adrole = "selected"; }
	
	print <<EOF;
	<form method=POST>
		<table border="0" width="100%" cellspacing="0" cellpadding="0">
			<tr bgcolor=#D0D0D0>
				<!-- <td>名前<td>学籍番号<td>チーム<td>開発担当<td>役割<td>ドキュメント番号<td>更新日時 -->
				<td>名前<td>チーム<td>開発担当<td>役割<td>ドキュメント番号<td>更新日時
			<tr bgcolor=#FFFFFF>
				<td><input type=text name=eName value="$namer">
				<!-- <td><input type=text name=eNum value="$num"> -->
				<td><input type=text name=eTeam value="$team">
				<td><select name=ePos>
						<option value="O" $opos>未定
						<option value="M" $mpos>メカニクス
						<option value="E" $epos>エレクトロニクス
						<option value="S" $spos>ソフトウェア
					</select>
				<td><select name=eRole>
						<option value="N" $nrole>
						<option value="P" $prole>プロジェクトマネージャ
						<option value="L" $lrole>チームリーダ
						<option value="D" $drole>ドキュメントマネージャ
						<option value="AD" $adrole>広報
					</select>
				<td><input type=text name=eDoc value="$doc" size=30>
				<td>$mtime
			<tr>
			<tr>
				<td align=right colspan=6><input type=hidden name=mode value="edit">
										  <input type=submit name=esSubmit value="+ 変更 +">
		</table>
	</form>
	<p>
	<table border="0" width="100%" cellspacing="0" cellpadding="0">
		<tr bgcolor=#D0D0D0>
			<!-- <td>日付<td>作業コード<td>作業内容<td>授業内作業(H)<td>授業外作業(H)<td>備考<td>操作 -->
			<td>日付<td>作業コード<td>作業内容<td>作業時間(H)<td>備考<td>操作
EOF
	#my($date, $code, $work, $h1, $h2, $note,$h1sum, $h2sum, @loglist) = undef;
	my($date, $code, $work, $h1, $note,$h1sum, @loglist) = undef;
	push @loglist, "<select name=InsPos>\n";
	
	for(my $i=1;$i<=$#data;$i++) {
		#($date, $code, $work, $h1, $h2, $note) = split("<>", $data[$i]);
		($date, $code, $work, $h1, $note) = split("<>", $data[$i]);
		$work =~ s/<br>/\n/g;
		print <<EOF;
		<tr>
			<form method=POST>
				<td><input type=text name=eDate value="$date" size=11></td>
				<td><input type=text name=eCode value="$code" size=6></td>
				<td><textarea wrap=soft name=eWork cols=30 rows=1>$work</textarea></td>
				<td><input type=text name=eH1   value="$h1" size=4></td>
				<!-- <td><input type=text name=eH2   value="$h2" size=4></td> -->
				<td><input type=text name=eNote value="$note"></td>
				<td><input type=hidden name=LogPos value="$i">
					<input type=hidden name=mode value=edit>
					<input type=submit name=ewChange value="変更">
					<input type=submit name=ewDelete value="削除"></td>
			</form>
		</tr>
EOF
	#	$h1 =~ s/[^0-9]//g;
		$h1sum += 0+$h1;
	#	$h2 =~ s/[^0-9]//g;
	#	$h2sum += 0+$h2;
		
		push @loglist, "\t\t\t\t\t<option value=\"$i\">$date\n";
	}
	push @loglist, "\t\t\t\t</select>\n";
	my $t = &fixedtime;
	print <<EOF;
		<tr>
			<td colspan=3 align=right><hr size=1 color=#D0D0D0></td>
			<td>$h1sum</td>
			<!-- <td>$h2sum</td> -->
			<td colspan=2><hr size=1 color=#D0D0D0></td>
		</tr>
		<tr bgcolor=#D0D0D0>
			<!-- <td>日付<td width=1%>作業コード<td>作業内容<td>授業内作業(H)<td>授業外作業(H)<td>備考<td nowrap>操作 -->
			<td>日付<td width=1%>作業コード<td>作業内容<td>作業時間(H)<td>備考<td nowrap>操作
		<tr>
			<form method=POST>
				<td rowspan=2><input type=text name=eDate value="$t" size=11></td>
				<td rowspan=2><select name=eCode width=10>
								<option value="01">01:ミーティング</option>
								<option value="02">02:ドキュメントレビュー</option>
								<option value="03">03:ドキュメント整備</option>
								<option value="10">10:MIRS解体</option>
								<option value="11">11:標準部品製造・試験</option>
								<option value="12">12:標準機機能試験</option>
								<option value="13">13:デモ競技プログラム開発</option>
								<option value="14">14:標準機統合試験</option>
								<option value="20">20:技術調査・製品企画</option>
								<option value="21">21:企画、システム提案、開発計画立案</option>
								<option value="22">22:システム基本設計</option>
								<option value="23">23:システム統合試験</option>
								<option value="30">30:メカ詳細設計</option>
								<option value="31">31:エレキ詳細設計</option>
								<option value="32">32:ソフト詳細設計</option>
								<option value="40">40:メカ製造・試験</option>
								<option value="41">41-エレキ製造・試験</option>
								<option value="42">42-ソフト実装・試験</option>
								<option value="50">50:発表会システム開発</option>
								<option value="51">51:社会実装実験</option>
								<option value="52">52:発表会準備</option>
								<option value="60">60:その他</option>
							   </select>
				<td rowspan=2><textarea wrap=soft name=eWork cols=30 rows=4></textarea></td>
				<td rowspan=2><input type=text name=eH1 size=4></td>
				<!-- <td rowspan=2><input type=text name=eH2 size=4></td> -->
				<td rowspan=2><input type=text name=eNote></td>
				<td><input type=hidden name=mode value=edit>
					<input type=submit name=ewAdd value="+ 追加 +">
		</tr>
		<tr>
			<td>@loglist<br>
				の前に<input type=submit name=ewInsert value="挿入">
			</td>
			</form>
		</tr>
	</table>
	<p>
EOF
		print <<EOF;
	<form method=POST>
		<table border="0" width="100%" cellspacing="0" cellpadding="0">
			<tr><td width=100%>
				<input type=hidden name="mode" value="view2">
				<input type=hidden name="user_name" value="$name">
				<input type=submit name="pSubmit" value="表示画面に進む">

		</table>
	</form>
EOF
	return;
}

# -------------------------------------------------------------------------- #

#	ChangeSettings - Change user settings.

sub ChangeSettings {
	#my($name, $num, $namer, $team, $pos, $role, $doc, $pass, $new, $errormes);
	my($name, $namer, $team, $pos, $role, $doc, $pass, $new, $errormes);
	$name  = &GetUser;
	$pass  = &GetPass;
	$namer = jcode( $q->param('eName') )->euc;
	#$num   = uc $q->param('eNum');
	$team  = uc $q->param('eTeam');
	$pos   = uc $q->param('ePos');
	$role   = uc $q->param('eRole');
	$doc   = uc $q->param('eDoc');

	$namer =~ s/\n|$tag_regex//g;
	#$num   =~ s/\n|$tag_regex//g;
	$team  =~ s/\n|$tag_regex//g;
	$pos   =~ s/\n|$tag_regex//g;
	$role   =~ s/\n|$tag_regex//g;
	$doc   =~ s/\n|$tag_regex//g;

	if ($name !~ /^\w{4,12}$/) {
		$errormes = "名前が不正です。";
#	}#elsif ($num !~ /^[A-Z]\d{3}$/) {
#		$errormes = "学籍番号が不正です。";
	} elsif ($team !~ /^MIRS\d{4}$/) {
		$errormes = "チームが不正です。";
	} elsif ($pos !~ /^(M|E|S|O)/) {
		$errormes = "開発担当が不正です。";
	} elsif ($role !~ /^(P|L|D|CS|AD|N)/) {
		$errormes = "役割が不正です。";
	} elsif ($doc !~ /^MIRS\d{4}-[A-Z]+-\d+$/) {
		$errormes = "ドキュメント番号が不正です。";
	}
	if ($errormes) {
		&error2("変更 - $errormes");
	}

	#$new = "$name<>$num<>$namer<>$team<>$pos<>$role<>$doc<>$pass<>\n";
	$new = "$name<>$namer<>$team<>$pos<>$role<>$doc<>$pass<>\n";

	if( &IsUserExists($name) ) {
		# WTF!
		open(READ,"$logdir/$name.log") or
			&error2("ログファイルが開けません。管理者に連絡してください。");
			@foo = <READ>;
			$foo[0] = $new;
		close(READ);
		open(WRITE,">$logdir/$name.log") or
			&error2("ログファイルが開けません。管理者に連絡してください。");
			print WRITE @foo;
		close(WRITE);
		&backto("$self?mode=edit");
	} else {
		&error2("ユーザーが存在しません。");
	}
	return;
}

# -------------------------------------------------------------------------- #

#	ChangeLog - Change user log data.

sub ChangeLog {
	#my($name, $date, $code, $work, $h1, $h2, $note, $logpos, $new);
	my($name, $date, $code, $work, $h1, $note, $logpos, $new);
	$name	= &GetUser;
	$date	= $q->param('eDate');
	$code	= uc $q->param('eCode');
	$work	= jcode( $q->param('eWork') )->euc;
	$h1		= $q->param('eH1');
	#$h2		= $q->param('eH2');
	$note	= jcode( $q->param('eNote') )->euc;
	$logpos	= $q->param('LogPos');

	$date	=~ s/\n|$tag_regex//g;
	$code	=~ s/\n|$tag_regex//g;
	$work	=~ s/$tag_regex//g;
	$work	=~ s/\n/<br>/g;
	#$h1		=~ s/\n|$tag_regex|[^0-9]//g;
	#$h2		=~ s/\n|$tag_regex|[^0-9]//g;
	$note	=~ s/\n|$tag_regex//g;
	
	#$new = "$date<>$code<>$work<>$h1<>$h2<>$note<>\n";
	$new = "$date<>$code<>$work<>$h1<>$note<>\n";

	if( &IsUserExists($name) ) {
		#if( ($work && $h1) || ($work && $h2) ) {
		if( ($work && $h1) ) {
			# WTF!
			open(READ,"$logdir/$name.log") or
				&error2("ログファイルが開けません。管理者に連絡してください。");
				@foo = <READ>;
				$foo[$logpos] = $new;
			close(READ);
			open(WRITE,">$logdir/$name.log") or
				&error2("ログファイルが開けません。管理者に連絡してください。");
				print WRITE @foo;
			close(WRITE);
		}
		&backto("$self?mode=edit");
	} else {
		&error2("ユーザーが存在しません。");
	}
	return;
}

# -------------------------------------------------------------------------- #

#	DeleteLog - Delete user log data.

sub DeleteLog {
	my $logpos = $q->param('LogPos');
	my $name   = &GetUser;
	
	if( &IsUserExists($name) ) {
		# WTF!
		open(READ,"$logdir/$name.log") or
			&error2("ログファイルが開けません。管理者に連絡してください。");
			@foo = <READ>;
			undef $foo[$logpos];
		close(READ);
		open(WRITE,">$logdir/$name.log") or
			&error2("ログファイルが開けません。管理者に連絡してください。");
			print WRITE @foo;
		close(WRITE);
		&backto("$self?mode=edit");
	} else {
		&error2("ユーザーが存在しません。");
	}
}

# -------------------------------------------------------------------------- #

#	AddLog - Add user log data.

sub AddLog {
	#my($name, $date, $code, $work, $h1, $h2, $note, $logpos, $new);
	my($name, $date, $code, $work, $h1, $note, $logpos, $new);
	$name	= &GetUser;
	$date	= $q->param('eDate');
	$code	= uc $q->param('eCode');
	$work	= jcode( $q->param('eWork') )->euc;
	$h1		= $q->param('eH1');
	#$h2		= $q->param('eH2');
	$note	= jcode( $q->param('eNote') )->euc;
	$logpos	= $q->param('LogPos');

	$date	=~ s/\n|$tag_regex//g;
	$code	=~ s/\n|$tag_regex//g;
	$work	=~ s/$tag_regex//g;
	$work	=~ s/\n/<br>/g;
	#$h1		=~ s/\n|$tag_regex|[^0-9]//g;
	#$h2		=~ s/\n|$tag_regex|[^0-9]//g;
	$note	=~ s/\n|$tag_regex//g;
	
	#$new = "$date<>$code<>$work<>$h1<>$h2<>$note<>\n";
	$new = "$date<>$code<>$work<>$h1<>$note<>\n";
	if( &IsUserExists($name) ) {
		#if( ($work && $h1) || ($work && $h2) ) {
		if( ($work && $h1) ) {
			# WTF!
			open(WRITE,">>$logdir/$name.log") or
				&error2("ログファイルが開けません。管理者に連絡してください。");
				print WRITE $new;
			close(WRITE);
		}
		&backto("$self?mode=edit");
	} else {
		&error2("ユーザーが存在しません。");
	}
	return;
}

# -------------------------------------------------------------------------- #

#	InsertLog - Insert user log data.

sub InsertLog {
	#my($name, $date, $code, $work, $h1, $h2, $note, $inspos, $new);
	my($name, $date, $code, $work, $h1, $note, $inspos, $new);
	$name	= &GetUser;
	$date	= $q->param('eDate');
	$code	= uc $q->param('eCode');
	$work	= jcode( $q->param('eWork') )->euc;
	$h1		= $q->param('eH1');
	#$h2		= $q->param('eH2');
	$note	= jcode( $q->param('eNote') )->euc;
	$inspos	= $q->param('InsPos');

	$date	=~ s/\n|$tag_regex//g;
	$code	=~ s/\n|$tag_regex//g;
	$work	=~ s/$tag_regex//g;
	$work	=~ s/\n/<br>/g;
	#$h1		=~ s/\n|$tag_regex|[^0-9]//g;
	#$h2		=~ s/\n|$tag_regex|[^0-9]//g;
	$note	=~ s/\n|$tag_regex//g;
	
	#$new = "$date<>$code<>$work<>$h1<>$h2<>$note<>\n";
	$new = "$date<>$code<>$work<>$h1<>$note<>\n";
	if( &IsUserExists($name) ) {
		#if( ($work && $h1) || ($work && $h2) ) {
		if( ($work && $h1) ) {
			# WTF!
			open(READ,"$logdir/$name.log") or
				&error2("ログファイルが開けません。管理者に連絡してください。");
				@foo = <READ>;
				$foo[$inspos] = $new . $foo[$inspos];
			close(READ);
			open(WRITE,">$logdir/$name.log") or
				&error2("ログファイルが開けません。管理者に連絡してください。");
				print WRITE @foo;
			close(WRITE);
		}
		&backto("$self?mode=edit");
	} else {
		&error2("ユーザーが存在しません。");
	}
	return;
}

# -------------------------------------------------------------------------- #

#	ShowAbout - Show version info etc etc...

sub ShowAbout {

	print <<EOF;
	<!-- About -->
	<table border="0" width="100%" cellspacing="0" cellpadding="0">
		<tr><td width=100%>
		<div class=title>このスクリプトについて</div>
		<div class=comment>
			<p>
			現在のバージョン：$ver<br>
			<hr size=1 color=#D0D0D0>
			このスクリプトは、若林一君の作成したMIRS0202作業記録用スクリプトを書き直したものです。<br>
			modified by S. Ushimaru (2004/6/10)
<!--
			意見、要望等は <a href="mailto:hajime\@eces.numazu-ct.ac.jp">hajime\@eces.numazu-ct.ac.jp</a> まで。
			<p>
			&#169; 2004- Hajime Wakabayashi
-->
			<p>
	</table>
EOF

	return;
}
