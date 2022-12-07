import pyparsing as pp  # make sure you have this installed (pyparsing==3.0.9)
import json
import copy


class QueryBuilder:
    def __init__(self, input=""):
        self.loadquery(input)

    def loadquery(self, input):
        if input == None or input == "":
            self.input = None
            self.input_to_list = None
            self.skills = None
        else:
            self.input = input
            self.input_list = QueryBuilder.string_to_list(self.input)
            self.skills = QueryBuilder.morpher(self.input_list)

    @staticmethod
    def string_to_list(input):
        parser = pp.nestedExpr("(", ")")
        try:
            return parser.parseString("(" + input + ")")
        except:
            print("Error!!!")
            raise Exception("Error, Please check the input!!")

    @staticmethod
    def morpher(x):
        result = []
        operand = []
        operator = ""

        for i in x:
            if type(i) is list or type(i) is pp.results.ParseResults:
                sublist = QueryBuilder.morpher(i)
                if operator == "":
                    if len(operand):
                        print("Error!!!")
                        raise Exception("Error, Please check the input!!")
                    else:
                        operand = sublist
                elif operator == "AND":
                    operator = ""
                    if len(operand):
                        temp = []
                        for item in operand:
                            for subitem in sublist:
                                temp.append(item + subitem)
                        operand = temp
                    else:
                        operand = sublist
                else:
                    operator = ""
                    result.extend(operand)
                    operand = sublist

            elif i not in {"AND", "OR"}:
                temp = [i.replace('"', "").replace("'", "")]

                if operator == "":
                    if len(operand):
                        print("Error!!!")
                        raise Exception("Error, Please check the input!!")
                    else:
                        operand.append(temp)
                elif operator == "AND":
                    operator = ""
                    if len(operand):
                        for item in operand:
                            item.extend(temp)
                    else:
                        operand.append(temp)
                else:
                    operator = ""
                    result.extend(operand)
                    operand = [temp]

            else:
                if operator == "" and len(operand) != 0:
                    operator = i
                else:
                    print("Error!!!")
                    raise Exception("Error, Please check the input!!")
        result.extend(operand)
        return result

    def to_mysql_using_like(self):
        if self.skills == None:
            return None
        skills = copy.deepcopy(self.skills)
        base_condition = ' text like "%{}%" '
        base_query = "select * from resume where "
        for item in skills:
            for i in range(len(item)):
                item[i] = base_condition.format(item[i].lower())
        for i in range(len(skills)):
            skills[i] = " (" + " and ".join(skills[i]) + ") "
        condition = " or ".join(skills)
        return base_query + condition

    def to_mysql(self):
        if self.skills == None:
            return None
        skills = copy.deepcopy(self.skills)
        base_condition = " match(text) against('{}' in Boolean mode)"
        base_query = "select * from resume where "
        for i in range(len(skills)):
            temp = ""
            for j in range(len(skills[i])):
                if " " in skills[i][j]:
                    temp += ' +"{}" '.format(skills[i][j])
                else:
                    temp += " +{} ".format(skills[i][j])
            skills[i] = temp
        for i in range(len(skills)):
            skills[i] = base_condition.format(skills[i].lower())
        condition = " or ".join(skills)
        return base_query + condition

    def to_mongoDB(self):
        if self.skills == None:
            return None
        skills = copy.deepcopy(self.skills)
        base_condition = '{{"text": {{"$regex": ".*{}.*", "$options": "i"}}}}'
        base_query = '{{"$or":[{}]}}'
        for i in range(len(skills)):
            for j in range(len(skills[i])):
                skills[i][j] = base_condition.format(skills[i][j].replace("+", "[+]"))
        for i in range(len(skills)):
            if len(skills[i]) == 1:
                skills[i] = skills[i][0]
            else:
                skills[i] = '{"$and":[' + ",".join(skills[i]) + "]}"
        if len(skills) == 1:
            query = skills[0]
        else:
            query = base_query.format(",".join(skills))
        return query

    def to_elasticsearch_direct(self):
        if self.input == None:
            return None
        base_query = {
            "query": {
                "query_string": {
                    "query": self.input,
                    "fields": ["text"],
                }
            }
        }
        return json.dumps(base_query)

    def to_elasticsearch(self):
        if self.skills == None:
            return None
        skills = copy.deepcopy(self.skills)
        base_condition1 = '"{}"'
        base_condition2 = "{}"
        base_query = {
            "query": {
                "query_string": {
                    "query": "",
                    "fields": ["text"],
                }
            }
        }
        print(skills)
        for item in skills:
            for i in range(len(item)):
                if " " in item[i]:
                    item[i] = base_condition1.format(item[i].lower())
                else:
                    item[i] = base_condition2.format(item[i].lower())
        for i in range(len(skills)):
            skills[i] = " (" + " AND ".join(skills[i]) + ") "
        condition = " OR ".join(skills)
        base_query["query"]["query_string"]["query"] = condition
        return json.dumps(base_query)

    def get_all(self):
        return {
            "input": self.input,
            "mysql": self.to_mysql(),
            "mysql_like": self.to_mysql_using_like(),
            "mongodb": self.to_mongoDB(),
            "elasticsearch": self.to_elasticsearch(),
            "elasticsearch_direct": self.to_elasticsearch_direct(),
        }


if __name__ == "__main__":
    qb = QueryBuilder("")
    qb.loadquery("(python AND  (Java AND Spring)) OR php")
    print("Raw mySQL\n", qb.to_mysql(), end="\n\n")
    print("Raw mySQL using LIKE clause\n", qb.to_mysql_using_like(), end="\n\n")
    print("MongoDB Query\n", qb.to_mongoDB(), end="\n\n")
    print("ElasticSearch Query\n", qb.to_elasticsearch(), end="\n\n")
    print(
        "ElasticSearch Query, direct build from input\n",
        qb.to_elasticsearch_direct(),
        end="\n\n",
    )
