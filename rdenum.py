import urllib
import json
import sys

GOOGLE_API_URL = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&{}"


if __name__ == "__main__":
    if len(sys.argv) > 1:
        founded_set = set()
        link = sys.argv[1]

        while True:
            excluded_q = "-site:" + " -site:".join(founded_set) if founded_set else ""
            full_q = urllib.urlencode({'q': "site:{} {}".format(link, excluded_q)})
            url = GOOGLE_API_URL.format(full_q)

            search_response = urllib.urlopen(url)
            results = json.loads(search_response.read())
            if not results['responseData']:
                print "[!] Error: {}".format(results['responseDetails'])
                break
            try:
                result_count = int(results['responseData']['cursor']['estimatedResultCount'])
                results = results['responseData']['results']
            except KeyError:
                break
            for result in results:
                new_link = result['url']
                if new_link.startswith('http://'):
                    clean_link = new_link[7:]
                    clean_link = clean_link.split('/')[0]
                elif new_link.startswith('https://'):
                    clean_link = new_link[8:]
                    clean_link = clean_link.split('/')[0]
                else:
                    print "[!] Invalid protocol: {}".format(new_link)
                    continue
                founded_set.add(clean_link)
        for founded in founded_set:
            print "[*] Founded: {}".format(founded)
    else:
        print "[!] Usage: {} <start_point>".format(__file__)