import xml.etree.ElementTree as ET
import re

xml = '''
<FIXML xsi:schemaLocation="http://www.finacle.com/fixml executeFinacleScript.xsd" xmlns="http://www.finacle.com/fixml"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <Header>
        <RequestHeader>
            <MessageKey>
                <RequestUUID>Req_1516077882977</RequestUUID>
                <ServiceRequestId>executeFinacleScript</ServiceRequestId>
                <ServiceRequestVersion>10.2</ServiceRequestVersion>
                <ChannelId>COR</ChannelId>
                <LanguageId/>
            </MessageKey>
            <RequestMessageInfo>
                <BankId/>
                <TimeZone/>
                <EntityId/>
                <EntityType/>
                <ArmCorrelationId/>
                <MessageDateTime>2018-00-16T10:14:42.976</MessageDateTime>
            </RequestMessageInfo>
            <Security>
                <Token>
                    <PasswordToken>
                        <UserId/>
                        <Password/>
                    </PasswordToken>
                </Token>
                <FICertToken/>
                <RealUserLoginSessionId/>
                <RealUser/>
                <RealUserPwd/>
                <SSOTransferToken/>
            </Security>
        </RequestHeader>
    </Header>
    <Body>
        <executeFinacleScriptRequest>
            <ExecuteFinacleScriptInputVO>
                <requestId>SMB_FI_SMS_Status_Maintenance.scr</requestId>
            </ExecuteFinacleScriptInputVO>
            <executeFinacleScript_CustomData>
                <custId>301241145</custId>
                <mobileNo>0777637433</mobileNo>
                <custStatus>Y</custStatus>
                <chgAcct>102960099600</chgAcct>
                <funcCode>A</funcCode>
            </executeFinacleScript_CustomData>
        </executeFinacleScriptRequest>
    </Body>
</FIXML>
'''

root = ET.fromstring(xml)

ESQL = ''

for parent in root:
    for child in parent:
        for child2 in child:
            for child3 in child2:
                if re.split('}', child2.tag)[1] == 'Security':
                    continue
                r = re.split('}', root.tag)[1]
                p = re.split('}', parent.tag)[1]
                c1 = re.split('}', child.tag)[1]
                c2 = re.split('}', child2.tag)[1]
                c3 = re.split('}', child3.tag)[1]
                t = child3.text

                if t is None:
                    ESQL += f"SET OutputRoot.XMLNSC.xmlns:{r}.xmlns:{p}.xmlns:{c1}.xmlns:{c2}.xmlns:{c3}.(XML.Content) = NULL;\n"
                else:
                    ESQL += f"SET OutputRoot.XMLNSC.xmlns:{r}.xmlns:{p}.xmlns:{c1}.xmlns:{c2}.xmlns:{c3} = {t};\n"

print(ESQL)
