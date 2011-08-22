import digg_api
import sys
import semantic_analysis as sa

try:
  granularity = int(sys.argv[1])
except:
  granularity = 20

if 'lsi' in sys.argv:
  lda = False
else:
  lda = True

# Actual digg titles
entries = digg_api.get_entries() #deterministic

result = sa.discover(entries, granularity=granularity, lda=lda)
print( sa.print_results(result) )

